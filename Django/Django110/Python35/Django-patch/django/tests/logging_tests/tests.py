# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import logging
import warnings

from admin_scripts.tests import AdminScriptTestCase

from django.conf import settings
from django.core import mail
from django.core.files.temp import NamedTemporaryFile
from django.db import connection
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.test.utils import LoggingCaptureMixin, patch_logger
from django.utils.deprecation import RemovedInNextVersionWarning
from django.utils.log import (
    DEFAULT_LOGGING, AdminEmailHandler, CallbackFilter, RequireDebugFalse,
    RequireDebugTrue,
)

from .logconfig import MyEmailBackend

# logging config prior to using filter with mail_admins
OLD_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


class LoggingFiltersTest(SimpleTestCase):
    def test_require_debug_false_filter(self):
        """
        Test the RequireDebugFalse filter class.
        """
        filter_ = RequireDebugFalse()

        with self.settings(DEBUG=True):
            self.assertIs(filter_.filter("record is not used"), False)

        with self.settings(DEBUG=False):
            self.assertIs(filter_.filter("record is not used"), True)

    def test_require_debug_true_filter(self):
        """
        Test the RequireDebugTrue filter class.
        """
        filter_ = RequireDebugTrue()

        with self.settings(DEBUG=True):
            self.assertIs(filter_.filter("record is not used"), True)

        with self.settings(DEBUG=False):
            self.assertIs(filter_.filter("record is not used"), False)


class SetupDefaultLoggingMixin(object):

    @classmethod
    def setUpClass(cls):
        super(SetupDefaultLoggingMixin, cls).setUpClass()
        cls._logging = settings.LOGGING
        logging.config.dictConfig(DEFAULT_LOGGING)

    @classmethod
    def tearDownClass(cls):
        super(SetupDefaultLoggingMixin, cls).tearDownClass()
        logging.config.dictConfig(cls._logging)


class DefaultLoggingTests(SetupDefaultLoggingMixin, LoggingCaptureMixin, SimpleTestCase):

    def test_django_logger(self):
        """
        The 'django' base logger only output anything when DEBUG=True.
        """
        self.logger.error("Hey, this is an error.")
        self.assertEqual(self.logger_output.getvalue(), '')

        with self.settings(DEBUG=True):
            self.logger.error("Hey, this is an error.")
            self.assertEqual(self.logger_output.getvalue(), 'Hey, this is an error.\n')

    @override_settings(DEBUG=True)
    def test_django_logger_warning(self):
        self.logger.warning('warning')
        self.assertEqual(self.logger_output.getvalue(), 'warning\n')

    @override_settings(DEBUG=True)
    def test_django_logger_info(self):
        self.logger.info('info')
        self.assertEqual(self.logger_output.getvalue(), 'info\n')

    @override_settings(DEBUG=True)
    def test_django_logger_debug(self):
        self.logger.debug('debug')
        self.assertEqual(self.logger_output.getvalue(), '')


@override_settings(DEBUG=True, ROOT_URLCONF='logging_tests.urls')
class HandlerLoggingTests(SetupDefaultLoggingMixin, LoggingCaptureMixin, SimpleTestCase):

    def test_page_found_no_warning(self):
        self.client.get('/innocent/')
        self.assertEqual(self.logger_output.getvalue(), '')

    def test_page_not_found_warning(self):
        self.client.get('/does_not_exist/')
        self.assertEqual(self.logger_output.getvalue(), 'Not Found: /does_not_exist/\n')


@override_settings(
    DEBUG=True,
    USE_I18N=True,
    LANGUAGES=[('en', 'English')],
    MIDDLEWARE=[
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
    ROOT_URLCONF='logging_tests.urls_i18n',
)
class I18nLoggingTests(SetupDefaultLoggingMixin, LoggingCaptureMixin, SimpleTestCase):

    def test_i18n_page_found_no_warning(self):
        self.client.get('/exists/')
        self.client.get('/en/exists/')
        self.assertEqual(self.logger_output.getvalue(), '')

    def test_i18n_page_not_found_warning(self):
        self.client.get('/this_does_not/')
        self.client.get('/en/nor_this/')
        self.assertEqual(self.logger_output.getvalue(), 'Not Found: /this_does_not/\nNot Found: /en/nor_this/\n')


class WarningLoggerTests(SimpleTestCase):
    """
    Tests that warnings output for RemovedInDjangoXXWarning (XX being the next
    Django version) is enabled and captured to the logging system
    """
    def setUp(self):
        # If tests are invoke with "-Wall" (or any -W flag actually) then
        # warning logging gets disabled (see configure_logging in django/utils/log.py).
        # However, these tests expect warnings to be logged, so manually force warnings
        # to the logs. Use getattr() here because the logging capture state is
        # undocumented and (I assume) brittle.
        self._old_capture_state = bool(getattr(logging, '_warnings_showwarning', False))
        logging.captureWarnings(True)

    def tearDown(self):
        # Reset warnings state.
        logging.captureWarnings(self._old_capture_state)

    @override_settings(DEBUG=True)
    def test_error_filter_still_raises(self):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'error',
                category=RemovedInNextVersionWarning
            )
            with self.assertRaises(RemovedInNextVersionWarning):
                warnings.warn('Foo Deprecated', RemovedInNextVersionWarning)


class CallbackFilterTest(SimpleTestCase):
    def test_sense(self):
        f_false = CallbackFilter(lambda r: False)
        f_true = CallbackFilter(lambda r: True)

        self.assertEqual(f_false.filter("record"), False)
        self.assertEqual(f_true.filter("record"), True)

    def test_passes_on_record(self):
        collector = []

        def _callback(record):
            collector.append(record)
            return True
        f = CallbackFilter(_callback)

        f.filter("a record")

        self.assertEqual(collector, ["a record"])


class AdminEmailHandlerTest(SimpleTestCase):
    logger = logging.getLogger('django')

    def get_admin_email_handler(self, logger):
        # Ensure that AdminEmailHandler does not get filtered out
        # even with DEBUG=True.
        admin_email_handler = [
            h for h in logger.handlers
            if h.__class__.__name__ == "AdminEmailHandler"
        ][0]
        return admin_email_handler

    def test_fail_silently(self):
        admin_email_handler = self.get_admin_email_handler(self.logger)
        self.assertTrue(admin_email_handler.connection().fail_silently)

    @override_settings(
        ADMINS=[('whatever admin', 'admin@example.com')],
        EMAIL_SUBJECT_PREFIX='-SuperAwesomeSubject-'
    )
    def test_accepts_args(self):
        """
        Ensure that user-supplied arguments and the EMAIL_SUBJECT_PREFIX
        setting are used to compose the email subject.
        Refs #16736.
        """
        message = "Custom message that says '%s' and '%s'"
        token1 = 'ping'
        token2 = 'pong'

        admin_email_handler = self.get_admin_email_handler(self.logger)
        # Backup then override original filters
        orig_filters = admin_email_handler.filters
        try:
            admin_email_handler.filters = []

            self.logger.error(message, token1, token2)

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].to, ['admin@example.com'])
            self.assertEqual(mail.outbox[0].subject,
                             "-SuperAwesomeSubject-ERROR: Custom message that says 'ping' and 'pong'")
        finally:
            # Restore original filters
            admin_email_handler.filters = orig_filters

    @override_settings(
        ADMINS=[('whatever admin', 'admin@example.com')],
        EMAIL_SUBJECT_PREFIX='-SuperAwesomeSubject-',
        INTERNAL_IPS=['127.0.0.1'],
    )
    def test_accepts_args_and_request(self):
        """
        Ensure that the subject is also handled if being
        passed a request object.
        """
        message = "Custom message that says '%s' and '%s'"
        token1 = 'ping'
        token2 = 'pong'

        admin_email_handler = self.get_admin_email_handler(self.logger)
        # Backup then override original filters
        orig_filters = admin_email_handler.filters
        try:
            admin_email_handler.filters = []
            rf = RequestFactory()
            request = rf.get('/')
            self.logger.error(
                message, token1, token2,
                extra={
                    'status_code': 403,
                    'request': request,
                }
            )
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].to, ['admin@example.com'])
            self.assertEqual(mail.outbox[0].subject,
                             "-SuperAwesomeSubject-ERROR (internal IP): Custom message that says 'ping' and 'pong'")
        finally:
            # Restore original filters
            admin_email_handler.filters = orig_filters

    @override_settings(
        ADMINS=[('admin', 'admin@example.com')],
        EMAIL_SUBJECT_PREFIX='',
        DEBUG=False,
    )
    def test_subject_accepts_newlines(self):
        """
        Ensure that newlines in email reports' subjects are escaped to avoid
        AdminErrorHandler to fail.
        Refs #17281.
        """
        message = 'Message \r\n with newlines'
        expected_subject = 'ERROR: Message \\r\\n with newlines'

        self.assertEqual(len(mail.outbox), 0)

        self.logger.error(message)

        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn('\n', mail.outbox[0].subject)
        self.assertNotIn('\r', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].subject, expected_subject)

    @override_settings(
        ADMINS=[('admin', 'admin@example.com')],
        DEBUG=False,
    )
    def test_uses_custom_email_backend(self):
        """
        Refs #19325
        """
        message = 'All work and no play makes Jack a dull boy'
        admin_email_handler = self.get_admin_email_handler(self.logger)
        mail_admins_called = {'called': False}

        def my_mail_admins(*args, **kwargs):
            connection = kwargs['connection']
            self.assertIsInstance(connection, MyEmailBackend)
            mail_admins_called['called'] = True

        # Monkeypatches
        orig_mail_admins = mail.mail_admins
        orig_email_backend = admin_email_handler.email_backend
        mail.mail_admins = my_mail_admins
        admin_email_handler.email_backend = (
            'logging_tests.logconfig.MyEmailBackend')

        try:
            self.logger.error(message)
            self.assertTrue(mail_admins_called['called'])
        finally:
            # Revert Monkeypatches
            mail.mail_admins = orig_mail_admins
            admin_email_handler.email_backend = orig_email_backend

    @override_settings(
        ADMINS=[('whatever admin', 'admin@example.com')],
    )
    def test_emit_non_ascii(self):
        """
        #23593 - AdminEmailHandler should allow Unicode characters in the
        request.
        """
        handler = self.get_admin_email_handler(self.logger)
        record = self.logger.makeRecord('name', logging.ERROR, 'function', 'lno', 'message', None, None)
        rf = RequestFactory()
        url_path = '/º'
        record.request = rf.get(url_path)
        handler.emit(record)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ['admin@example.com'])
        self.assertEqual(msg.subject, "[Django] ERROR (EXTERNAL IP): message")
        self.assertIn("Report at %s" % url_path, msg.body)

    @override_settings(
        MANAGERS=[('manager', 'manager@example.com')],
        DEBUG=False,
    )
    def test_customize_send_mail_method(self):
        class ManagerEmailHandler(AdminEmailHandler):
            def send_mail(self, subject, message, *args, **kwargs):
                mail.mail_managers(subject, message, *args, connection=self.connection(), **kwargs)

        handler = ManagerEmailHandler()
        record = self.logger.makeRecord('name', logging.ERROR, 'function', 'lno', 'message', None, None)
        self.assertEqual(len(mail.outbox), 0)
        handler.emit(record)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['manager@example.com'])

    @override_settings(ALLOWED_HOSTS='example.com')
    def test_disallowed_host_doesnt_crash(self):
        admin_email_handler = self.get_admin_email_handler(self.logger)
        old_include_html = admin_email_handler.include_html

        # Text email
        admin_email_handler.include_html = False
        try:
            self.client.get('/', HTTP_HOST='evil.com')
        finally:
            admin_email_handler.include_html = old_include_html

        # HTML email
        admin_email_handler.include_html = True
        try:
            self.client.get('/', HTTP_HOST='evil.com')
        finally:
            admin_email_handler.include_html = old_include_html


class SettingsConfigTest(AdminScriptTestCase):
    """
    Test that accessing settings in a custom logging handler does not trigger
    a circular import error.
    """
    def setUp(self):
        log_config = """{
    'version': 1,
    'handlers': {
        'custom_handler': {
            'level': 'INFO',
            'class': 'logging_tests.logconfig.MyHandler',
        }
    }
}"""
        self.write_settings('settings.py', sdict={'LOGGING': log_config})

    def tearDown(self):
        self.remove_settings('settings.py')

    def test_circular_dependency(self):
        # validate is just an example command to trigger settings configuration
        out, err = self.run_manage(['check'])
        self.assertNoOutput(err)
        self.assertOutput(out, "System check identified no issues (0 silenced).")


def dictConfig(config):
    dictConfig.called = True
dictConfig.called = False


class SetupConfigureLogging(SimpleTestCase):
    """
    Test that calling django.setup() initializes the logging configuration.
    """
    @override_settings(LOGGING_CONFIG='logging_tests.tests.dictConfig',
                       LOGGING=OLD_LOGGING)
    def test_configure_initializes_logging(self):
        from django import setup
        setup()
        self.assertTrue(dictConfig.called)


@override_settings(DEBUG=True, ROOT_URLCONF='logging_tests.urls')
class SecurityLoggerTest(SimpleTestCase):

    def test_suspicious_operation_creates_log_message(self):
        with patch_logger('django.security.SuspiciousOperation', 'error') as calls:
            self.client.get('/suspicious/')
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0], 'dubious')

    def test_suspicious_operation_uses_sublogger(self):
        with patch_logger('django.security.DisallowedHost', 'error') as calls:
            self.client.get('/suspicious_spec/')
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0], 'dubious')

    @override_settings(
        ADMINS=[('admin', 'admin@example.com')],
        DEBUG=False,
    )
    def test_suspicious_email_admins(self):
        self.client.get('/suspicious/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Report at /suspicious/', mail.outbox[0].body)


class SettingsCustomLoggingTest(AdminScriptTestCase):
    """
    Test that using a logging defaults are still applied when using a custom
    callable in LOGGING_CONFIG (i.e., logging.config.fileConfig).
    """
    def setUp(self):
        logging_conf = """
[loggers]
keys=root
[handlers]
keys=stream
[formatters]
keys=simple
[logger_root]
handlers=stream
[handler_stream]
class=StreamHandler
formatter=simple
args=(sys.stdout,)
[formatter_simple]
format=%(message)s
"""
        self.temp_file = NamedTemporaryFile()
        self.temp_file.write(logging_conf.encode('utf-8'))
        self.temp_file.flush()
        sdict = {'LOGGING_CONFIG': '"logging.config.fileConfig"',
                 'LOGGING': 'r"%s"' % self.temp_file.name}
        self.write_settings('settings.py', sdict=sdict)

    def tearDown(self):
        self.temp_file.close()
        self.remove_settings('settings.py')

    def test_custom_logging(self):
        out, err = self.run_manage(['check'])
        self.assertNoOutput(err)
        self.assertOutput(out, "System check identified no issues (0 silenced).")


class SchemaLoggerTests(SimpleTestCase):

    def test_extra_args(self):
        editor = connection.schema_editor(collect_sql=True)
        sql = "SELECT * FROM foo WHERE id in (%s, %s)"
        params = [42, 1337]
        with patch_logger('django.db.backends.schema', 'debug', log_kwargs=True) as logger:
            editor.execute(sql, params)
        self.assertEqual(
            logger,
            [(
                'SELECT * FROM foo WHERE id in (%s, %s); (params [42, 1337])',
                {'extra': {
                    'sql': 'SELECT * FROM foo WHERE id in (%s, %s)',
                    'params': [42, 1337],
                }},
            )]
        )

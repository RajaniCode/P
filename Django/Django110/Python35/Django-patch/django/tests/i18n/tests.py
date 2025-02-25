# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import decimal
import gettext as gettext_module
import os
import pickle
from contextlib import contextmanager
from importlib import import_module
from threading import local
from unittest import skipUnless

from django import forms
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.template import Context, Template, TemplateSyntaxError
from django.test import (
    RequestFactory, SimpleTestCase, TestCase, override_settings,
)
from django.utils import six, translation
from django.utils._os import upath
from django.utils.formats import (
    date_format, get_format, get_format_modules, iter_format_modules, localize,
    localize_input, reset_format_cache, sanitize_separators, time_format,
)
from django.utils.numberformat import format as nformat
from django.utils.safestring import SafeBytes, SafeString, SafeText, mark_safe
from django.utils.six import PY3
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, activate, check_for_language, deactivate,
    get_language, get_language_bidi, get_language_from_request,
    get_language_info, gettext, gettext_lazy, ngettext_lazy, npgettext,
    npgettext_lazy, pgettext, pgettext_lazy, string_concat, to_locale,
    trans_real, ugettext, ugettext_lazy, ungettext, ungettext_lazy,
)

from .forms import CompanyForm, I18nForm, SelectDateForm
from .models import Company, TestModel

here = os.path.dirname(os.path.abspath(upath(__file__)))
extended_locale_paths = settings.LOCALE_PATHS + [
    os.path.join(here, 'other', 'locale'),
]


@contextmanager
def patch_formats(lang, **settings):
    from django.utils.formats import _format_cache

    # Populate _format_cache with temporary values
    for key, value in settings.items():
        _format_cache[(key, lang)] = value
    try:
        yield
    finally:
        reset_format_cache()


class TranslationTests(SimpleTestCase):

    @translation.override('fr')
    def test_plural(self):
        """
        Test plurals with ungettext. French differs from English in that 0 is singular.
        """
        self.assertEqual(ungettext("%d year", "%d years", 0) % 0, "0 année")
        self.assertEqual(ungettext("%d year", "%d years", 2) % 2, "2 années")
        self.assertEqual(ungettext("%(size)d byte", "%(size)d bytes", 0) % {'size': 0}, "0 octet")
        self.assertEqual(ungettext("%(size)d byte", "%(size)d bytes", 2) % {'size': 2}, "2 octets")

    def test_override(self):
        activate('de')
        try:
            with translation.override('pl'):
                self.assertEqual(get_language(), 'pl')
            self.assertEqual(get_language(), 'de')
            with translation.override(None):
                self.assertIsNone(get_language())
                with translation.override('pl'):
                    pass
                self.assertIsNone(get_language())
            self.assertEqual(get_language(), 'de')
        finally:
            deactivate()

    def test_override_decorator(self):

        @translation.override('pl')
        def func_pl():
            self.assertEqual(get_language(), 'pl')

        @translation.override(None)
        def func_none():
            self.assertIsNone(get_language())

        try:
            activate('de')
            func_pl()
            self.assertEqual(get_language(), 'de')
            func_none()
            self.assertEqual(get_language(), 'de')
        finally:
            deactivate()

    def test_override_exit(self):
        """
        Test that the language restored is the one used when the function was
        called, not the one used when the decorator was initialized. refs #23381
        """
        activate('fr')

        @translation.override('pl')
        def func_pl():
            pass
        deactivate()

        try:
            activate('en')
            func_pl()
            self.assertEqual(get_language(), 'en')
        finally:
            deactivate()

    def test_lazy_objects(self):
        """
        Format string interpolation should work with *_lazy objects.
        """
        s = ugettext_lazy('Add %(name)s')
        d = {'name': 'Ringo'}
        self.assertEqual('Add Ringo', s % d)
        with translation.override('de', deactivate=True):
            self.assertEqual('Ringo hinzuf\xfcgen', s % d)
            with translation.override('pl'):
                self.assertEqual('Dodaj Ringo', s % d)

        # It should be possible to compare *_lazy objects.
        s1 = ugettext_lazy('Add %(name)s')
        self.assertEqual(s, s1)
        s2 = gettext_lazy('Add %(name)s')
        s3 = gettext_lazy('Add %(name)s')
        self.assertEqual(s2, s3)
        self.assertEqual(s, s2)
        s4 = ugettext_lazy('Some other string')
        self.assertNotEqual(s, s4)

    @skipUnless(six.PY2, "No more bytestring translations on PY3")
    def test_bytestrings(self):
        """gettext() returns a bytestring if input is bytestring."""

        # Using repr() to check translated text and type
        self.assertEqual(repr(gettext(b"Time")), repr(b"Time"))
        self.assertEqual(repr(gettext("Time")), repr("Time"))

        with translation.override('de', deactivate=True):
            self.assertEqual(repr(gettext(b"Time")), repr(b"Zeit"))
            self.assertEqual(repr(gettext("Time")), repr(b"Zeit"))

    @skipUnless(six.PY2, "No more bytestring translations on PY3")
    def test_lazy_and_bytestrings(self):
        # On Python 2, (n)gettext_lazy should not transform a bytestring to unicode
        self.assertEqual(gettext_lazy(b"test").upper(), b"TEST")
        self.assertEqual((ngettext_lazy(b"%d test", b"%d tests") % 1).upper(), b"1 TEST")

        # Other versions of lazy functions always return unicode
        self.assertEqual(ugettext_lazy(b"test").upper(), "TEST")
        self.assertEqual((ungettext_lazy(b"%d test", b"%d tests") % 1).upper(), "1 TEST")
        self.assertEqual(pgettext_lazy(b"context", b"test").upper(), "TEST")
        self.assertEqual(
            (npgettext_lazy(b"context", b"%d test", b"%d tests") % 1).upper(),
            "1 TEST"
        )

    def test_lazy_pickle(self):
        s1 = ugettext_lazy("test")
        self.assertEqual(six.text_type(s1), "test")
        s2 = pickle.loads(pickle.dumps(s1))
        self.assertEqual(six.text_type(s2), "test")

    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_ungettext_lazy(self):
        simple_with_format = ungettext_lazy('%d good result', '%d good results')
        simple_str_with_format = ngettext_lazy(str('%d good result'), str('%d good results'))
        simple_context_with_format = npgettext_lazy('Exclamation', '%d good result', '%d good results')
        simple_without_format = ungettext_lazy('good result', 'good results')
        with translation.override('de'):
            self.assertEqual(simple_with_format % 1, '1 gutes Resultat')
            self.assertEqual(simple_with_format % 4, '4 guten Resultate')
            self.assertEqual(simple_str_with_format % 1, str('1 gutes Resultat'))
            self.assertEqual(simple_str_with_format % 4, str('4 guten Resultate'))
            self.assertEqual(simple_context_with_format % 1, '1 gutes Resultat!')
            self.assertEqual(simple_context_with_format % 4, '4 guten Resultate!')
            self.assertEqual(simple_without_format % 1, 'gutes Resultat')
            self.assertEqual(simple_without_format % 4, 'guten Resultate')

        complex_nonlazy = ungettext_lazy('Hi %(name)s, %(num)d good result', 'Hi %(name)s, %(num)d good results', 4)
        complex_deferred = ungettext_lazy(
            'Hi %(name)s, %(num)d good result', 'Hi %(name)s, %(num)d good results', 'num'
        )
        complex_str_nonlazy = ngettext_lazy(
            str('Hi %(name)s, %(num)d good result'), str('Hi %(name)s, %(num)d good results'), 4
        )
        complex_str_deferred = ngettext_lazy(
            str('Hi %(name)s, %(num)d good result'), str('Hi %(name)s, %(num)d good results'), 'num'
        )
        complex_context_nonlazy = npgettext_lazy(
            'Greeting', 'Hi %(name)s, %(num)d good result', 'Hi %(name)s, %(num)d good results', 4
        )
        complex_context_deferred = npgettext_lazy(
            'Greeting', 'Hi %(name)s, %(num)d good result', 'Hi %(name)s, %(num)d good results', 'num'
        )
        with translation.override('de'):
            self.assertEqual(complex_nonlazy % {'num': 4, 'name': 'Jim'}, 'Hallo Jim, 4 guten Resultate')
            self.assertEqual(complex_deferred % {'name': 'Jim', 'num': 1}, 'Hallo Jim, 1 gutes Resultat')
            self.assertEqual(complex_deferred % {'name': 'Jim', 'num': 5}, 'Hallo Jim, 5 guten Resultate')
            with six.assertRaisesRegex(self, KeyError, 'Your dictionary lacks key.*'):
                complex_deferred % {'name': 'Jim'}
            self.assertEqual(complex_str_nonlazy % {'num': 4, 'name': 'Jim'}, str('Hallo Jim, 4 guten Resultate'))
            self.assertEqual(complex_str_deferred % {'name': 'Jim', 'num': 1}, str('Hallo Jim, 1 gutes Resultat'))
            self.assertEqual(complex_str_deferred % {'name': 'Jim', 'num': 5}, str('Hallo Jim, 5 guten Resultate'))
            with six.assertRaisesRegex(self, KeyError, 'Your dictionary lacks key.*'):
                complex_str_deferred % {'name': 'Jim'}
            self.assertEqual(complex_context_nonlazy % {'num': 4, 'name': 'Jim'}, 'Willkommen Jim, 4 guten Resultate')
            self.assertEqual(complex_context_deferred % {'name': 'Jim', 'num': 1}, 'Willkommen Jim, 1 gutes Resultat')
            self.assertEqual(complex_context_deferred % {'name': 'Jim', 'num': 5}, 'Willkommen Jim, 5 guten Resultate')
            with six.assertRaisesRegex(self, KeyError, 'Your dictionary lacks key.*'):
                complex_context_deferred % {'name': 'Jim'}

    @skipUnless(six.PY2, "PY3 doesn't have distinct int and long types")
    def test_ungettext_lazy_long(self):
        """
        Regression test for #22820: int and long should be treated alike in ungettext_lazy.
        """
        result = ungettext_lazy('%(name)s has %(num)d good result', '%(name)s has %(num)d good results', 4)
        self.assertEqual(result % {'name': 'Joe', 'num': 4}, "Joe has 4 good results")
        # Now with a long
        result = ungettext_lazy(
            '%(name)s has %(num)d good result', '%(name)s has %(num)d good results',
            long(4)   # NOQA: long undefined on PY3
        )
        self.assertEqual(result % {'name': 'Joe', 'num': 4}, "Joe has 4 good results")

    def test_ungettext_lazy_bool(self):
        self.assertTrue(ungettext_lazy('%d good result', '%d good results'))
        self.assertFalse(ungettext_lazy('', ''))

    def test_ungettext_lazy_pickle(self):
        s1 = ungettext_lazy('%d good result', '%d good results')
        self.assertEqual(s1 % 1, '1 good result')
        self.assertEqual(s1 % 8, '8 good results')
        s2 = pickle.loads(pickle.dumps(s1))
        self.assertEqual(s2 % 1, '1 good result')
        self.assertEqual(s2 % 8, '8 good results')

    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_pgettext(self):
        trans_real._active = local()
        trans_real._translations = {}
        with translation.override('de'):
            self.assertEqual(pgettext("unexisting", "May"), "May")
            self.assertEqual(pgettext("month name", "May"), "Mai")
            self.assertEqual(pgettext("verb", "May"), "Kann")
            self.assertEqual(npgettext("search", "%d result", "%d results", 4) % 4, "4 Resultate")

    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_template_tags_pgettext(self):
        """
        Ensure that message contexts are taken into account the {% trans %} and
        {% blocktrans %} template tags.
        Refs #14806.
        """
        trans_real._active = local()
        trans_real._translations = {}
        with translation.override('de'):

            # {% trans %} -----------------------------------

            # Inexisting context...
            t = Template('{% load i18n %}{% trans "May" context "unexisting" %}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'May')

            # Existing context...
            # Using a literal
            t = Template('{% load i18n %}{% trans "May" context "month name" %}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Mai')
            t = Template('{% load i18n %}{% trans "May" context "verb" %}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Kann')

            # Using a variable
            t = Template('{% load i18n %}{% trans "May" context message_context %}')
            rendered = t.render(Context({'message_context': 'month name'}))
            self.assertEqual(rendered, 'Mai')
            t = Template('{% load i18n %}{% trans "May" context message_context %}')
            rendered = t.render(Context({'message_context': 'verb'}))
            self.assertEqual(rendered, 'Kann')

            # Using a filter
            t = Template('{% load i18n %}{% trans "May" context message_context|lower %}')
            rendered = t.render(Context({'message_context': 'MONTH NAME'}))
            self.assertEqual(rendered, 'Mai')
            t = Template('{% load i18n %}{% trans "May" context message_context|lower %}')
            rendered = t.render(Context({'message_context': 'VERB'}))
            self.assertEqual(rendered, 'Kann')

            # Using 'as'
            t = Template('{% load i18n %}{% trans "May" context "month name" as var %}Value: {{ var }}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Value: Mai')
            t = Template('{% load i18n %}{% trans "May" as var context "verb" %}Value: {{ var }}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Value: Kann')

            # {% blocktrans %} ------------------------------

            # Inexisting context...
            t = Template('{% load i18n %}{% blocktrans context "unexisting" %}May{% endblocktrans %}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'May')

            # Existing context...
            # Using a literal
            t = Template('{% load i18n %}{% blocktrans context "month name" %}May{% endblocktrans %}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Mai')
            t = Template('{% load i18n %}{% blocktrans context "verb" %}May{% endblocktrans %}')
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Kann')

            # Using a variable
            t = Template('{% load i18n %}{% blocktrans context message_context %}May{% endblocktrans %}')
            rendered = t.render(Context({'message_context': 'month name'}))
            self.assertEqual(rendered, 'Mai')
            t = Template('{% load i18n %}{% blocktrans context message_context %}May{% endblocktrans %}')
            rendered = t.render(Context({'message_context': 'verb'}))
            self.assertEqual(rendered, 'Kann')

            # Using a filter
            t = Template('{% load i18n %}{% blocktrans context message_context|lower %}May{% endblocktrans %}')
            rendered = t.render(Context({'message_context': 'MONTH NAME'}))
            self.assertEqual(rendered, 'Mai')
            t = Template('{% load i18n %}{% blocktrans context message_context|lower %}May{% endblocktrans %}')
            rendered = t.render(Context({'message_context': 'VERB'}))
            self.assertEqual(rendered, 'Kann')

            # Using 'count'
            t = Template(
                '{% load i18n %}{% blocktrans count number=1 context "super search" %}'
                '{{ number }} super result{% plural %}{{ number }} super results{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, '1 Super-Ergebnis')
            t = Template(
                '{% load i18n %}{% blocktrans count number=2 context "super search" %}{{ number }}'
                ' super result{% plural %}{{ number }} super results{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, '2 Super-Ergebnisse')
            t = Template(
                '{% load i18n %}{% blocktrans context "other super search" count number=1 %}'
                '{{ number }} super result{% plural %}{{ number }} super results{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, '1 anderen Super-Ergebnis')
            t = Template(
                '{% load i18n %}{% blocktrans context "other super search" count number=2 %}'
                '{{ number }} super result{% plural %}{{ number }} super results{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, '2 andere Super-Ergebnisse')

            # Using 'with'
            t = Template(
                '{% load i18n %}{% blocktrans with num_comments=5 context "comment count" %}'
                'There are {{ num_comments }} comments{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Es gibt 5 Kommentare')
            t = Template(
                '{% load i18n %}{% blocktrans with num_comments=5 context "other comment count" %}'
                'There are {{ num_comments }} comments{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Andere: Es gibt 5 Kommentare')

            # Using trimmed
            t = Template(
                '{% load i18n %}{% blocktrans trimmed %}\n\nThere\n\t are 5  '
                '\n\n   comments\n{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, 'There are 5 comments')
            t = Template(
                '{% load i18n %}{% blocktrans with num_comments=5 context "comment count" trimmed %}\n\n'
                'There are  \t\n  \t {{ num_comments }} comments\n\n{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, 'Es gibt 5 Kommentare')
            t = Template(
                '{% load i18n %}{% blocktrans context "other super search" count number=2 trimmed %}\n'
                '{{ number }} super \n result{% plural %}{{ number }} super results{% endblocktrans %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, '2 andere Super-Ergebnisse')

            # Mis-uses
            with self.assertRaises(TemplateSyntaxError):
                Template('{% load i18n %}{% blocktrans context with month="May" %}{{ month }}{% endblocktrans %}')
            with self.assertRaises(TemplateSyntaxError):
                Template('{% load i18n %}{% blocktrans context %}{% endblocktrans %}')
            with self.assertRaises(TemplateSyntaxError):
                Template(
                    '{% load i18n %}{% blocktrans count number=2 context %}'
                    '{{ number }} super result{% plural %}{{ number }}'
                    ' super results{% endblocktrans %}'
                )

    def test_string_concat(self):
        """
        six.text_type(string_concat(...)) should not raise a TypeError - #4796
        """
        self.assertEqual('django', six.text_type(string_concat("dja", "ngo")))

    def test_empty_value(self):
        """
        Empty value must stay empty after being translated (#23196).
        """
        with translation.override('de'):
            self.assertEqual("", ugettext(""))
            self.assertEqual(str(""), gettext(str("")))
            s = mark_safe("")
            self.assertEqual(s, ugettext(s))

    def test_safe_status(self):
        """
        Translating a string requiring no auto-escaping shouldn't change the "safe" status.
        """
        s = mark_safe(str('Password'))
        self.assertEqual(SafeString, type(s))
        with translation.override('de', deactivate=True):
            self.assertEqual(SafeText, type(ugettext(s)))
        self.assertEqual('aPassword', SafeText('a') + s)
        self.assertEqual('Passworda', s + SafeText('a'))
        self.assertEqual('Passworda', s + mark_safe('a'))
        self.assertEqual('aPassword', mark_safe('a') + s)
        self.assertEqual('as', mark_safe('a') + mark_safe('s'))

    def test_maclines(self):
        """
        Translations on files with mac or dos end of lines will be converted
        to unix eof in .po catalogs, and they have to match when retrieved
        """
        ca_translation = trans_real.translation('ca')
        ca_translation._catalog['Mac\nEOF\n'] = 'Catalan Mac\nEOF\n'
        ca_translation._catalog['Win\nEOF\n'] = 'Catalan Win\nEOF\n'
        with translation.override('ca', deactivate=True):
            self.assertEqual('Catalan Mac\nEOF\n', ugettext('Mac\rEOF\r'))
            self.assertEqual('Catalan Win\nEOF\n', ugettext('Win\r\nEOF\r\n'))

    def test_to_locale(self):
        """
        Tests the to_locale function and the special case of Serbian Latin
        (refs #12230 and r11299)
        """
        self.assertEqual(to_locale('en-us'), 'en_US')
        self.assertEqual(to_locale('sr-lat'), 'sr_Lat')

    def test_to_language(self):
        """
        Test the to_language function
        """
        self.assertEqual(trans_real.to_language('en_US'), 'en-us')
        self.assertEqual(trans_real.to_language('sr_Lat'), 'sr-lat')

    def test_language_bidi(self):
        self.assertIs(get_language_bidi(), False)
        with translation.override(None):
            self.assertIs(get_language_bidi(), False)

    @override_settings(LOCALE_PATHS=[os.path.join(here, 'other', 'locale')])
    def test_bad_placeholder_1(self):
        """
        Error in translation file should not crash template rendering
        (%(person)s is translated as %(personne)s in fr.po)
        Refs #16516.
        """
        with translation.override('fr'):
            t = Template('{% load i18n %}{% blocktrans %}My name is {{ person }}.{% endblocktrans %}')
            rendered = t.render(Context({'person': 'James'}))
            self.assertEqual(rendered, 'My name is James.')

    @override_settings(LOCALE_PATHS=[os.path.join(here, 'other', 'locale')])
    def test_bad_placeholder_2(self):
        """
        Error in translation file should not crash template rendering
        (%(person) misses a 's' in fr.po, causing the string formatting to fail)
        Refs #18393.
        """
        with translation.override('fr'):
            t = Template('{% load i18n %}{% blocktrans %}My other name is {{ person }}.{% endblocktrans %}')
            rendered = t.render(Context({'person': 'James'}))
            self.assertEqual(rendered, 'My other name is James.')


class TranslationThreadSafetyTests(SimpleTestCase):

    def setUp(self):
        self._old_language = get_language()
        self._translations = trans_real._translations

        # here we rely on .split() being called inside the _fetch()
        # in trans_real.translation()
        class sideeffect_str(str):
            def split(self, *args, **kwargs):
                res = str.split(self, *args, **kwargs)
                trans_real._translations['en-YY'] = None
                return res

        trans_real._translations = {sideeffect_str('en-XX'): None}

    def tearDown(self):
        trans_real._translations = self._translations
        activate(self._old_language)

    def test_bug14894_translation_activate_thread_safety(self):
        translation_count = len(trans_real._translations)
        # May raise RuntimeError if translation.activate() isn't thread-safe.
        translation.activate('pl')
        # make sure sideeffect_str actually added a new translation
        self.assertLess(translation_count, len(trans_real._translations))


@override_settings(USE_L10N=True)
class FormattingTests(SimpleTestCase):

    def setUp(self):
        super(FormattingTests, self).setUp()
        self.n = decimal.Decimal('66666.666')
        self.f = 99999.999
        self.d = datetime.date(2009, 12, 31)
        self.dt = datetime.datetime(2009, 12, 31, 20, 50)
        self.t = datetime.time(10, 15, 48)
        self.l = 10000 if PY3 else long(10000)  # NOQA: long undefined on PY3
        self.ctxt = Context({
            'n': self.n,
            't': self.t,
            'd': self.d,
            'dt': self.dt,
            'f': self.f,
            'l': self.l,
        })

    def test_locale_independent(self):
        """
        Localization of numbers
        """
        with self.settings(USE_THOUSAND_SEPARATOR=False):
            self.assertEqual('66666.66', nformat(self.n, decimal_sep='.', decimal_pos=2, grouping=3, thousand_sep=','))
            self.assertEqual('66666A6', nformat(self.n, decimal_sep='A', decimal_pos=1, grouping=1, thousand_sep='B'))
            self.assertEqual('66666', nformat(self.n, decimal_sep='X', decimal_pos=0, grouping=1, thousand_sep='Y'))

        with self.settings(USE_THOUSAND_SEPARATOR=True):
            self.assertEqual(
                '66,666.66',
                nformat(self.n, decimal_sep='.', decimal_pos=2, grouping=3, thousand_sep=',')
            )
            self.assertEqual(
                '6B6B6B6B6A6',
                nformat(self.n, decimal_sep='A', decimal_pos=1, grouping=1, thousand_sep='B')
            )
            self.assertEqual('-66666.6', nformat(-66666.666, decimal_sep='.', decimal_pos=1))
            self.assertEqual('-66666.0', nformat(int('-66666'), decimal_sep='.', decimal_pos=1))
            self.assertEqual('10000.0', nformat(self.l, decimal_sep='.', decimal_pos=1))
            self.assertEqual(
                '10,00,00,000.00',
                nformat(100000000.00, decimal_sep='.', decimal_pos=2, grouping=(3, 2, 0), thousand_sep=',')
            )
            self.assertEqual(
                '1,0,00,000,0000.00',
                nformat(10000000000.00, decimal_sep='.', decimal_pos=2, grouping=(4, 3, 2, 1, 0), thousand_sep=',')
            )
            self.assertEqual(
                '10000,00,000.00',
                nformat(1000000000.00, decimal_sep='.', decimal_pos=2, grouping=(3, 2, -1), thousand_sep=',')
            )
            # This unusual grouping/force_grouping combination may be triggered by the intcomma filter (#17414)
            self.assertEqual('10000', nformat(self.l, decimal_sep='.', decimal_pos=0, grouping=0, force_grouping=True))

            # date filter
            self.assertEqual('31.12.2009 в 20:50', Template('{{ dt|date:"d.m.Y в H:i" }}').render(self.ctxt))
            self.assertEqual('⌚ 10:15', Template('{{ t|time:"⌚ H:i" }}').render(self.ctxt))

    @override_settings(USE_L10N=False)
    def test_l10n_disabled(self):
        """
        Catalan locale with format i18n disabled translations will be used,
        but not formats
        """
        with translation.override('ca', deactivate=True):
            self.maxDiff = 3000
            self.assertEqual('N j, Y', get_format('DATE_FORMAT'))
            self.assertEqual(0, get_format('FIRST_DAY_OF_WEEK'))
            self.assertEqual('.', get_format('DECIMAL_SEPARATOR'))
            self.assertEqual('10:15 a.m.', time_format(self.t))
            self.assertEqual('des. 31, 2009', date_format(self.d))
            self.assertEqual('desembre 2009', date_format(self.d, 'YEAR_MONTH_FORMAT'))
            self.assertEqual('12/31/2009 8:50 p.m.', date_format(self.dt, 'SHORT_DATETIME_FORMAT'))
            self.assertEqual('No localizable', localize('No localizable'))
            self.assertEqual('66666.666', localize(self.n))
            self.assertEqual('99999.999', localize(self.f))
            self.assertEqual('10000', localize(self.l))
            self.assertEqual('des. 31, 2009', localize(self.d))
            self.assertEqual('des. 31, 2009, 8:50 p.m.', localize(self.dt))
            self.assertEqual('66666.666', Template('{{ n }}').render(self.ctxt))
            self.assertEqual('99999.999', Template('{{ f }}').render(self.ctxt))
            self.assertEqual('des. 31, 2009', Template('{{ d }}').render(self.ctxt))
            self.assertEqual('des. 31, 2009, 8:50 p.m.', Template('{{ dt }}').render(self.ctxt))
            self.assertEqual('66666.67', Template('{{ n|floatformat:2 }}').render(self.ctxt))
            self.assertEqual('100000.0', Template('{{ f|floatformat }}').render(self.ctxt))
            self.assertEqual('10:15 a.m.', Template('{{ t|time:"TIME_FORMAT" }}').render(self.ctxt))
            self.assertEqual('12/31/2009', Template('{{ d|date:"SHORT_DATE_FORMAT" }}').render(self.ctxt))
            self.assertEqual(
                '12/31/2009 8:50 p.m.', Template('{{ dt|date:"SHORT_DATETIME_FORMAT" }}').render(self.ctxt)
            )

            form = I18nForm({
                'decimal_field': '66666,666',
                'float_field': '99999,999',
                'date_field': '31/12/2009',
                'datetime_field': '31/12/2009 20:50',
                'time_field': '20:50',
                'integer_field': '1.234',
            })
            self.assertFalse(form.is_valid())
            self.assertEqual(['Introdu\xefu un n\xfamero.'], form.errors['float_field'])
            self.assertEqual(['Introdu\xefu un n\xfamero.'], form.errors['decimal_field'])
            self.assertEqual(['Introdu\xefu una data v\xe0lida.'], form.errors['date_field'])
            self.assertEqual(['Introdu\xefu una data/hora v\xe0lides.'], form.errors['datetime_field'])
            self.assertEqual(['Introdu\xefu un n\xfamero sencer.'], form.errors['integer_field'])

            form2 = SelectDateForm({
                'date_field_month': '12',
                'date_field_day': '31',
                'date_field_year': '2009'
            })
            self.assertTrue(form2.is_valid())
            self.assertEqual(datetime.date(2009, 12, 31), form2.cleaned_data['date_field'])
            self.assertHTMLEqual(
                '<select name="mydate_month" id="id_mydate_month">'
                '<option value="0">---</option>'
                '<option value="1">gener</option>'
                '<option value="2">febrer</option>'
                '<option value="3">mar\xe7</option>'
                '<option value="4">abril</option>'
                '<option value="5">maig</option>'
                '<option value="6">juny</option>'
                '<option value="7">juliol</option>'
                '<option value="8">agost</option>'
                '<option value="9">setembre</option>'
                '<option value="10">octubre</option>'
                '<option value="11">novembre</option>'
                '<option value="12" selected="selected">desembre</option>'
                '</select>'
                '<select name="mydate_day" id="id_mydate_day">'
                '<option value="0">---</option>'
                '<option value="1">1</option>'
                '<option value="2">2</option>'
                '<option value="3">3</option>'
                '<option value="4">4</option>'
                '<option value="5">5</option>'
                '<option value="6">6</option>'
                '<option value="7">7</option>'
                '<option value="8">8</option>'
                '<option value="9">9</option>'
                '<option value="10">10</option>'
                '<option value="11">11</option>'
                '<option value="12">12</option>'
                '<option value="13">13</option>'
                '<option value="14">14</option>'
                '<option value="15">15</option>'
                '<option value="16">16</option>'
                '<option value="17">17</option>'
                '<option value="18">18</option>'
                '<option value="19">19</option>'
                '<option value="20">20</option>'
                '<option value="21">21</option>'
                '<option value="22">22</option>'
                '<option value="23">23</option>'
                '<option value="24">24</option>'
                '<option value="25">25</option>'
                '<option value="26">26</option>'
                '<option value="27">27</option>'
                '<option value="28">28</option>'
                '<option value="29">29</option>'
                '<option value="30">30</option>'
                '<option value="31" selected="selected">31</option>'
                '</select>'
                '<select name="mydate_year" id="id_mydate_year">'
                '<option value="0">---</option>'
                '<option value="2009" selected="selected">2009</option>'
                '<option value="2010">2010</option>'
                '<option value="2011">2011</option>'
                '<option value="2012">2012</option>'
                '<option value="2013">2013</option>'
                '<option value="2014">2014</option>'
                '<option value="2015">2015</option>'
                '<option value="2016">2016</option>'
                '<option value="2017">2017</option>'
                '<option value="2018">2018</option>'
                '</select>',
                forms.SelectDateWidget(years=range(2009, 2019)).render('mydate', datetime.date(2009, 12, 31))
            )

            # We shouldn't change the behavior of the floatformat filter re:
            # thousand separator and grouping when USE_L10N is False even
            # if the USE_THOUSAND_SEPARATOR, NUMBER_GROUPING and
            # THOUSAND_SEPARATOR settings are specified
            with self.settings(USE_THOUSAND_SEPARATOR=True, NUMBER_GROUPING=1, THOUSAND_SEPARATOR='!'):
                self.assertEqual('66666.67', Template('{{ n|floatformat:2 }}').render(self.ctxt))
                self.assertEqual('100000.0', Template('{{ f|floatformat }}').render(self.ctxt))

    def test_false_like_locale_formats(self):
        """
        Ensure that the active locale's formats take precedence over the
        default settings even if they would be interpreted as False in a
        conditional test (e.g. 0 or empty string).
        Refs #16938.
        """
        with patch_formats('fr', THOUSAND_SEPARATOR='', FIRST_DAY_OF_WEEK=0):
            with translation.override('fr'):
                with self.settings(USE_THOUSAND_SEPARATOR=True, THOUSAND_SEPARATOR='!'):
                    self.assertEqual('', get_format('THOUSAND_SEPARATOR'))
                    # Even a second time (after the format has been cached)...
                    self.assertEqual('', get_format('THOUSAND_SEPARATOR'))

                with self.settings(FIRST_DAY_OF_WEEK=1):
                    self.assertEqual(0, get_format('FIRST_DAY_OF_WEEK'))
                    # Even a second time (after the format has been cached)...
                    self.assertEqual(0, get_format('FIRST_DAY_OF_WEEK'))

    def test_l10n_enabled(self):
        self.maxDiff = 3000
        # Catalan locale
        with translation.override('ca', deactivate=True):
            self.assertEqual('j \d\e F \d\e Y', get_format('DATE_FORMAT'))
            self.assertEqual(1, get_format('FIRST_DAY_OF_WEEK'))
            self.assertEqual(',', get_format('DECIMAL_SEPARATOR'))
            self.assertEqual('10:15', time_format(self.t))
            self.assertEqual('31 de desembre de 2009', date_format(self.d))
            self.assertEqual('desembre del 2009', date_format(self.d, 'YEAR_MONTH_FORMAT'))
            self.assertEqual('31/12/2009 20:50', date_format(self.dt, 'SHORT_DATETIME_FORMAT'))
            self.assertEqual('No localizable', localize('No localizable'))

            with self.settings(USE_THOUSAND_SEPARATOR=True):
                self.assertEqual('66.666,666', localize(self.n))
                self.assertEqual('99.999,999', localize(self.f))
                self.assertEqual('10.000', localize(self.l))
                self.assertEqual('True', localize(True))

            with self.settings(USE_THOUSAND_SEPARATOR=False):
                self.assertEqual('66666,666', localize(self.n))
                self.assertEqual('99999,999', localize(self.f))
                self.assertEqual('10000', localize(self.l))
                self.assertEqual('31 de desembre de 2009', localize(self.d))
                self.assertEqual('31 de desembre de 2009 a les 20:50', localize(self.dt))

            with self.settings(USE_THOUSAND_SEPARATOR=True):
                self.assertEqual('66.666,666', Template('{{ n }}').render(self.ctxt))
                self.assertEqual('99.999,999', Template('{{ f }}').render(self.ctxt))
                self.assertEqual('10.000', Template('{{ l }}').render(self.ctxt))

            with self.settings(USE_THOUSAND_SEPARATOR=True):
                form3 = I18nForm({
                    'decimal_field': '66.666,666',
                    'float_field': '99.999,999',
                    'date_field': '31/12/2009',
                    'datetime_field': '31/12/2009 20:50',
                    'time_field': '20:50',
                    'integer_field': '1.234',
                })
                self.assertTrue(form3.is_valid())
                self.assertEqual(decimal.Decimal('66666.666'), form3.cleaned_data['decimal_field'])
                self.assertEqual(99999.999, form3.cleaned_data['float_field'])
                self.assertEqual(datetime.date(2009, 12, 31), form3.cleaned_data['date_field'])
                self.assertEqual(datetime.datetime(2009, 12, 31, 20, 50), form3.cleaned_data['datetime_field'])
                self.assertEqual(datetime.time(20, 50), form3.cleaned_data['time_field'])
                self.assertEqual(1234, form3.cleaned_data['integer_field'])

            with self.settings(USE_THOUSAND_SEPARATOR=False):
                self.assertEqual('66666,666', Template('{{ n }}').render(self.ctxt))
                self.assertEqual('99999,999', Template('{{ f }}').render(self.ctxt))
                self.assertEqual('31 de desembre de 2009', Template('{{ d }}').render(self.ctxt))
                self.assertEqual('31 de desembre de 2009 a les 20:50', Template('{{ dt }}').render(self.ctxt))
                self.assertEqual('66666,67', Template('{{ n|floatformat:2 }}').render(self.ctxt))
                self.assertEqual('100000,0', Template('{{ f|floatformat }}').render(self.ctxt))
                self.assertEqual('10:15', Template('{{ t|time:"TIME_FORMAT" }}').render(self.ctxt))
                self.assertEqual('31/12/2009', Template('{{ d|date:"SHORT_DATE_FORMAT" }}').render(self.ctxt))
                self.assertEqual(
                    '31/12/2009 20:50',
                    Template('{{ dt|date:"SHORT_DATETIME_FORMAT" }}').render(self.ctxt)
                )
                self.assertEqual(date_format(datetime.datetime.now(), "DATE_FORMAT"),
                                 Template('{% now "DATE_FORMAT" %}').render(self.ctxt))

            with self.settings(USE_THOUSAND_SEPARATOR=False):
                form4 = I18nForm({
                    'decimal_field': '66666,666',
                    'float_field': '99999,999',
                    'date_field': '31/12/2009',
                    'datetime_field': '31/12/2009 20:50',
                    'time_field': '20:50',
                    'integer_field': '1234',
                })
                self.assertTrue(form4.is_valid())
                self.assertEqual(decimal.Decimal('66666.666'), form4.cleaned_data['decimal_field'])
                self.assertEqual(99999.999, form4.cleaned_data['float_field'])
                self.assertEqual(datetime.date(2009, 12, 31), form4.cleaned_data['date_field'])
                self.assertEqual(datetime.datetime(2009, 12, 31, 20, 50), form4.cleaned_data['datetime_field'])
                self.assertEqual(datetime.time(20, 50), form4.cleaned_data['time_field'])
                self.assertEqual(1234, form4.cleaned_data['integer_field'])

            form5 = SelectDateForm({
                'date_field_month': '12',
                'date_field_day': '31',
                'date_field_year': '2009'
            })
            self.assertTrue(form5.is_valid())
            self.assertEqual(datetime.date(2009, 12, 31), form5.cleaned_data['date_field'])
            self.assertHTMLEqual(
                '<select name="mydate_day" id="id_mydate_day">'
                '<option value="0">---</option>'
                '<option value="1">1</option>'
                '<option value="2">2</option>'
                '<option value="3">3</option>'
                '<option value="4">4</option>'
                '<option value="5">5</option>'
                '<option value="6">6</option>'
                '<option value="7">7</option>'
                '<option value="8">8</option>'
                '<option value="9">9</option>'
                '<option value="10">10</option>'
                '<option value="11">11</option>'
                '<option value="12">12</option>'
                '<option value="13">13</option>'
                '<option value="14">14</option>'
                '<option value="15">15</option>'
                '<option value="16">16</option>'
                '<option value="17">17</option>'
                '<option value="18">18</option>'
                '<option value="19">19</option>'
                '<option value="20">20</option>'
                '<option value="21">21</option>'
                '<option value="22">22</option>'
                '<option value="23">23</option>'
                '<option value="24">24</option>'
                '<option value="25">25</option>'
                '<option value="26">26</option>'
                '<option value="27">27</option>'
                '<option value="28">28</option>'
                '<option value="29">29</option>'
                '<option value="30">30</option>'
                '<option value="31" selected="selected">31</option>'
                '</select>'
                '<select name="mydate_month" id="id_mydate_month">'
                '<option value="0">---</option>'
                '<option value="1">gener</option>'
                '<option value="2">febrer</option>'
                '<option value="3">mar\xe7</option>'
                '<option value="4">abril</option>'
                '<option value="5">maig</option>'
                '<option value="6">juny</option>'
                '<option value="7">juliol</option>'
                '<option value="8">agost</option>'
                '<option value="9">setembre</option>'
                '<option value="10">octubre</option>'
                '<option value="11">novembre</option>'
                '<option value="12" selected="selected">desembre</option>'
                '</select>'
                '<select name="mydate_year" id="id_mydate_year">'
                '<option value="0">---</option>'
                '<option value="2009" selected="selected">2009</option>'
                '<option value="2010">2010</option>'
                '<option value="2011">2011</option>'
                '<option value="2012">2012</option>'
                '<option value="2013">2013</option>'
                '<option value="2014">2014</option>'
                '<option value="2015">2015</option>'
                '<option value="2016">2016</option>'
                '<option value="2017">2017</option>'
                '<option value="2018">2018</option>'
                '</select>',
                forms.SelectDateWidget(years=range(2009, 2019)).render('mydate', datetime.date(2009, 12, 31))
            )

        # Russian locale (with E as month)
        with translation.override('ru', deactivate=True):
            self.assertHTMLEqual(
                '<select name="mydate_day" id="id_mydate_day">'
                '<option value="0">---</option>'
                '<option value="1">1</option>'
                '<option value="2">2</option>'
                '<option value="3">3</option>'
                '<option value="4">4</option>'
                '<option value="5">5</option>'
                '<option value="6">6</option>'
                '<option value="7">7</option>'
                '<option value="8">8</option>'
                '<option value="9">9</option>'
                '<option value="10">10</option>'
                '<option value="11">11</option>'
                '<option value="12">12</option>'
                '<option value="13">13</option>'
                '<option value="14">14</option>'
                '<option value="15">15</option>'
                '<option value="16">16</option>'
                '<option value="17">17</option>'
                '<option value="18">18</option>'
                '<option value="19">19</option>'
                '<option value="20">20</option>'
                '<option value="21">21</option>'
                '<option value="22">22</option>'
                '<option value="23">23</option>'
                '<option value="24">24</option>'
                '<option value="25">25</option>'
                '<option value="26">26</option>'
                '<option value="27">27</option>'
                '<option value="28">28</option>'
                '<option value="29">29</option>'
                '<option value="30">30</option>'
                '<option value="31" selected="selected">31</option>'
                '</select>'
                '<select name="mydate_month" id="id_mydate_month">'
                '<option value="0">---</option>'
                '<option value="1">\u042f\u043d\u0432\u0430\u0440\u044c</option>'
                '<option value="2">\u0424\u0435\u0432\u0440\u0430\u043b\u044c</option>'
                '<option value="3">\u041c\u0430\u0440\u0442</option>'
                '<option value="4">\u0410\u043f\u0440\u0435\u043b\u044c</option>'
                '<option value="5">\u041c\u0430\u0439</option>'
                '<option value="6">\u0418\u044e\u043d\u044c</option>'
                '<option value="7">\u0418\u044e\u043b\u044c</option>'
                '<option value="8">\u0410\u0432\u0433\u0443\u0441\u0442</option>'
                '<option value="9">\u0421\u0435\u043d\u0442\u044f\u0431\u0440\u044c</option>'
                '<option value="10">\u041e\u043a\u0442\u044f\u0431\u0440\u044c</option>'
                '<option value="11">\u041d\u043e\u044f\u0431\u0440\u044c</option>'
                '<option value="12" selected="selected">\u0414\u0435\u043a\u0430\u0431\u0440\u044c</option>'
                '</select>'
                '<select name="mydate_year" id="id_mydate_year">'
                '<option value="0">---</option>'
                '<option value="2009" selected="selected">2009</option>'
                '<option value="2010">2010</option>'
                '<option value="2011">2011</option>'
                '<option value="2012">2012</option>'
                '<option value="2013">2013</option>'
                '<option value="2014">2014</option>'
                '<option value="2015">2015</option>'
                '<option value="2016">2016</option>'
                '<option value="2017">2017</option>'
                '<option value="2018">2018</option>'
                '</select>',
                forms.SelectDateWidget(years=range(2009, 2019)).render('mydate', datetime.date(2009, 12, 31))
            )

        # English locale
        with translation.override('en', deactivate=True):
            self.assertEqual('N j, Y', get_format('DATE_FORMAT'))
            self.assertEqual(0, get_format('FIRST_DAY_OF_WEEK'))
            self.assertEqual('.', get_format('DECIMAL_SEPARATOR'))
            self.assertEqual('Dec. 31, 2009', date_format(self.d))
            self.assertEqual('December 2009', date_format(self.d, 'YEAR_MONTH_FORMAT'))
            self.assertEqual('12/31/2009 8:50 p.m.', date_format(self.dt, 'SHORT_DATETIME_FORMAT'))
            self.assertEqual('No localizable', localize('No localizable'))

            with self.settings(USE_THOUSAND_SEPARATOR=True):
                self.assertEqual('66,666.666', localize(self.n))
                self.assertEqual('99,999.999', localize(self.f))
                self.assertEqual('10,000', localize(self.l))

            with self.settings(USE_THOUSAND_SEPARATOR=False):
                self.assertEqual('66666.666', localize(self.n))
                self.assertEqual('99999.999', localize(self.f))
                self.assertEqual('10000', localize(self.l))
                self.assertEqual('Dec. 31, 2009', localize(self.d))
                self.assertEqual('Dec. 31, 2009, 8:50 p.m.', localize(self.dt))

            with self.settings(USE_THOUSAND_SEPARATOR=True):
                self.assertEqual('66,666.666', Template('{{ n }}').render(self.ctxt))
                self.assertEqual('99,999.999', Template('{{ f }}').render(self.ctxt))
                self.assertEqual('10,000', Template('{{ l }}').render(self.ctxt))

            with self.settings(USE_THOUSAND_SEPARATOR=False):
                self.assertEqual('66666.666', Template('{{ n }}').render(self.ctxt))
                self.assertEqual('99999.999', Template('{{ f }}').render(self.ctxt))
                self.assertEqual('Dec. 31, 2009', Template('{{ d }}').render(self.ctxt))
                self.assertEqual('Dec. 31, 2009, 8:50 p.m.', Template('{{ dt }}').render(self.ctxt))
                self.assertEqual('66666.67', Template('{{ n|floatformat:2 }}').render(self.ctxt))
                self.assertEqual('100000.0', Template('{{ f|floatformat }}').render(self.ctxt))
                self.assertEqual('12/31/2009', Template('{{ d|date:"SHORT_DATE_FORMAT" }}').render(self.ctxt))
                self.assertEqual(
                    '12/31/2009 8:50 p.m.',
                    Template('{{ dt|date:"SHORT_DATETIME_FORMAT" }}').render(self.ctxt)
                )

            form5 = I18nForm({
                'decimal_field': '66666.666',
                'float_field': '99999.999',
                'date_field': '12/31/2009',
                'datetime_field': '12/31/2009 20:50',
                'time_field': '20:50',
                'integer_field': '1234',
            })
            self.assertTrue(form5.is_valid())
            self.assertEqual(decimal.Decimal('66666.666'), form5.cleaned_data['decimal_field'])
            self.assertEqual(99999.999, form5.cleaned_data['float_field'])
            self.assertEqual(datetime.date(2009, 12, 31), form5.cleaned_data['date_field'])
            self.assertEqual(datetime.datetime(2009, 12, 31, 20, 50), form5.cleaned_data['datetime_field'])
            self.assertEqual(datetime.time(20, 50), form5.cleaned_data['time_field'])
            self.assertEqual(1234, form5.cleaned_data['integer_field'])

            form6 = SelectDateForm({
                'date_field_month': '12',
                'date_field_day': '31',
                'date_field_year': '2009'
            })
            self.assertTrue(form6.is_valid())
            self.assertEqual(datetime.date(2009, 12, 31), form6.cleaned_data['date_field'])
            self.assertHTMLEqual(
                '<select name="mydate_month" id="id_mydate_month">'
                '<option value="0">---</option>'
                '<option value="1">January</option>'
                '<option value="2">February</option>'
                '<option value="3">March</option>'
                '<option value="4">April</option>'
                '<option value="5">May</option>'
                '<option value="6">June</option>'
                '<option value="7">July</option>'
                '<option value="8">August</option>'
                '<option value="9">September</option>'
                '<option value="10">October</option>'
                '<option value="11">November</option>'
                '<option value="12" selected="selected">December</option>'
                '</select>'
                '<select name="mydate_day" id="id_mydate_day">'
                '<option value="0">---</option>'
                '<option value="1">1</option>'
                '<option value="2">2</option>'
                '<option value="3">3</option>'
                '<option value="4">4</option>'
                '<option value="5">5</option>'
                '<option value="6">6</option>'
                '<option value="7">7</option>'
                '<option value="8">8</option>'
                '<option value="9">9</option>'
                '<option value="10">10</option>'
                '<option value="11">11</option>'
                '<option value="12">12</option>'
                '<option value="13">13</option>'
                '<option value="14">14</option>'
                '<option value="15">15</option>'
                '<option value="16">16</option>'
                '<option value="17">17</option>'
                '<option value="18">18</option>'
                '<option value="19">19</option>'
                '<option value="20">20</option>'
                '<option value="21">21</option>'
                '<option value="22">22</option>'
                '<option value="23">23</option>'
                '<option value="24">24</option>'
                '<option value="25">25</option>'
                '<option value="26">26</option>'
                '<option value="27">27</option>'
                '<option value="28">28</option>'
                '<option value="29">29</option>'
                '<option value="30">30</option>'
                '<option value="31" selected="selected">31</option>'
                '</select>'
                '<select name="mydate_year" id="id_mydate_year">'
                '<option value="0">---</option>'
                '<option value="2009" selected="selected">2009</option>'
                '<option value="2010">2010</option>'
                '<option value="2011">2011</option>'
                '<option value="2012">2012</option>'
                '<option value="2013">2013</option>'
                '<option value="2014">2014</option>'
                '<option value="2015">2015</option>'
                '<option value="2016">2016</option>'
                '<option value="2017">2017</option>'
                '<option value="2018">2018</option>'
                '</select>',
                forms.SelectDateWidget(years=range(2009, 2019)).render('mydate', datetime.date(2009, 12, 31))
            )

    def test_sub_locales(self):
        """
        Check if sublocales fall back to the main locale
        """
        with self.settings(USE_THOUSAND_SEPARATOR=True):
            with translation.override('de-at', deactivate=True):
                self.assertEqual('66.666,666', Template('{{ n }}').render(self.ctxt))
            with translation.override('es-us', deactivate=True):
                self.assertEqual('31 de Diciembre de 2009', date_format(self.d))

    def test_localized_input(self):
        """
        Tests if form input is correctly localized
        """
        self.maxDiff = 1200
        with translation.override('de-at', deactivate=True):
            form6 = CompanyForm({
                'name': 'acme',
                'date_added': datetime.datetime(2009, 12, 31, 6, 0, 0),
                'cents_paid': decimal.Decimal('59.47'),
                'products_delivered': 12000,
            })
            self.assertTrue(form6.is_valid())
            self.assertHTMLEqual(
                form6.as_ul(),
                '<li><label for="id_name">Name:</label>'
                '<input id="id_name" type="text" name="name" value="acme" maxlength="50" required /></li>'
                '<li><label for="id_date_added">Date added:</label>'
                '<input type="text" name="date_added" value="31.12.2009 06:00:00" id="id_date_added" required /></li>'
                '<li><label for="id_cents_paid">Cents paid:</label>'
                '<input type="text" name="cents_paid" value="59,47" id="id_cents_paid" required /></li>'
                '<li><label for="id_products_delivered">Products delivered:</label>'
                '<input type="text" name="products_delivered" value="12000" id="id_products_delivered" required />'
                '</li>'
            )
            self.assertEqual(localize_input(datetime.datetime(2009, 12, 31, 6, 0, 0)), '31.12.2009 06:00:00')
            self.assertEqual(datetime.datetime(2009, 12, 31, 6, 0, 0), form6.cleaned_data['date_added'])
            with self.settings(USE_THOUSAND_SEPARATOR=True):
                # Checking for the localized "products_delivered" field
                self.assertInHTML(
                    '<input type="text" name="products_delivered" '
                    'value="12.000" id="id_products_delivered" required />',
                    form6.as_ul()
                )

    def test_localized_input_func(self):
        with self.settings(USE_THOUSAND_SEPARATOR=True):
            self.assertEqual(localize_input(True), 'True')

    def test_sanitize_separators(self):
        """
        Tests django.utils.formats.sanitize_separators.
        """
        # Non-strings are untouched
        self.assertEqual(sanitize_separators(123), 123)

        with translation.override('ru', deactivate=True):
            # Russian locale has non-breaking space (\xa0) as thousand separator
            # Check that usual space is accepted too when sanitizing inputs
            with self.settings(USE_THOUSAND_SEPARATOR=True):
                self.assertEqual(sanitize_separators('1\xa0234\xa0567'), '1234567')
                self.assertEqual(sanitize_separators('77\xa0777,777'), '77777.777')
                self.assertEqual(sanitize_separators('12 345'), '12345')
                self.assertEqual(sanitize_separators('77 777,777'), '77777.777')
            with self.settings(USE_THOUSAND_SEPARATOR=True, USE_L10N=False):
                self.assertEqual(sanitize_separators('12\xa0345'), '12\xa0345')

        with patch_formats(get_language(), THOUSAND_SEPARATOR='.', DECIMAL_SEPARATOR=','):
            with self.settings(USE_THOUSAND_SEPARATOR=True):
                self.assertEqual(sanitize_separators('10.234'), '10234')
                # Suspicion that user entered dot as decimal separator (#22171)
                self.assertEqual(sanitize_separators('10.10'), '10.10')

    def test_iter_format_modules(self):
        """
        Tests the iter_format_modules function.
        """
        # Importing some format modules so that we can compare the returned
        # modules with these expected modules
        default_mod = import_module('django.conf.locale.de.formats')
        test_mod = import_module('i18n.other.locale.de.formats')
        test_mod2 = import_module('i18n.other2.locale.de.formats')

        with translation.override('de-at', deactivate=True):
            # Should return the correct default module when no setting is set
            self.assertEqual(list(iter_format_modules('de')), [default_mod])

            # When the setting is a string, should return the given module and
            # the default module
            self.assertEqual(
                list(iter_format_modules('de', 'i18n.other.locale')),
                [test_mod, default_mod])

            # When setting is a list of strings, should return the given
            # modules and the default module
            self.assertEqual(
                list(iter_format_modules('de', ['i18n.other.locale', 'i18n.other2.locale'])),
                [test_mod, test_mod2, default_mod])

    def test_iter_format_modules_stability(self):
        """
        Tests the iter_format_modules function always yields format modules in
        a stable and correct order in presence of both base ll and ll_CC formats.
        """
        en_format_mod = import_module('django.conf.locale.en.formats')
        en_gb_format_mod = import_module('django.conf.locale.en_GB.formats')
        self.assertEqual(list(iter_format_modules('en-gb')), [en_gb_format_mod, en_format_mod])

    def test_get_format_modules_lang(self):
        with translation.override('de', deactivate=True):
            self.assertEqual('.', get_format('DECIMAL_SEPARATOR', lang='en'))

    def test_get_format_modules_stability(self):
        with self.settings(FORMAT_MODULE_PATH='i18n.other.locale'):
            with translation.override('de', deactivate=True):
                old = str("%r") % get_format_modules(reverse=True)
                new = str("%r") % get_format_modules(reverse=True)  # second try
                self.assertEqual(new, old, 'Value returned by get_formats_modules() must be preserved between calls.')

    def test_localize_templatetag_and_filter(self):
        """
        Tests the {% localize %} templatetag
        """
        context = Context({'value': 3.14})
        template1 = Template(
            '{% load l10n %}{% localize %}{{ value }}{% endlocalize %};'
            '{% localize on %}{{ value }}{% endlocalize %}'
        )
        template2 = Template("{% load l10n %}{{ value }};{% localize off %}{{ value }};{% endlocalize %}{{ value }}")
        template3 = Template('{% load l10n %}{{ value }};{{ value|unlocalize }}')
        template4 = Template('{% load l10n %}{{ value }};{{ value|localize }}')
        output1 = '3,14;3,14'
        output2 = '3,14;3.14;3,14'
        output3 = '3,14;3.14'
        output4 = '3.14;3,14'
        with translation.override('de', deactivate=True):
            with self.settings(USE_L10N=False):
                self.assertEqual(template1.render(context), output1)
                self.assertEqual(template4.render(context), output4)
            with self.settings(USE_L10N=True):
                self.assertEqual(template1.render(context), output1)
                self.assertEqual(template2.render(context), output2)
                self.assertEqual(template3.render(context), output3)

    def test_localized_as_text_as_hidden_input(self):
        """
        Tests if form input with 'as_hidden' or 'as_text' is correctly localized. Ticket #18777
        """
        self.maxDiff = 1200

        with translation.override('de-at', deactivate=True):
            template = Template('{% load l10n %}{{ form.date_added }}; {{ form.cents_paid }}')
            template_as_text = Template('{% load l10n %}{{ form.date_added.as_text }}; {{ form.cents_paid.as_text }}')
            template_as_hidden = Template(
                '{% load l10n %}{{ form.date_added.as_hidden }}; {{ form.cents_paid.as_hidden }}'
            )
            form = CompanyForm({
                'name': 'acme',
                'date_added': datetime.datetime(2009, 12, 31, 6, 0, 0),
                'cents_paid': decimal.Decimal('59.47'),
                'products_delivered': 12000,
            })
            context = Context({'form': form})
            self.assertTrue(form.is_valid())

            self.assertHTMLEqual(
                template.render(context),
                '<input id="id_date_added" name="date_added" type="text" value="31.12.2009 06:00:00" required />;'
                '<input id="id_cents_paid" name="cents_paid" type="text" value="59,47" required />'
            )
            self.assertHTMLEqual(
                template_as_text.render(context),
                '<input id="id_date_added" name="date_added" type="text" value="31.12.2009 06:00:00" required />;'
                ' <input id="id_cents_paid" name="cents_paid" type="text" value="59,47" required />'
            )
            self.assertHTMLEqual(
                template_as_hidden.render(context),
                '<input id="id_date_added" name="date_added" type="hidden" value="31.12.2009 06:00:00" />;'
                '<input id="id_cents_paid" name="cents_paid" type="hidden" value="59,47" />'
            )

    def test_format_arbitrary_settings(self):
        self.assertEqual(get_format('DEBUG'), 'DEBUG')

    def test_get_custom_format(self):
        with self.settings(FORMAT_MODULE_PATH='i18n.other.locale'):
            with translation.override('fr', deactivate=True):
                self.assertEqual('d/m/Y CUSTOM', get_format('CUSTOM_DAY_FORMAT'))


class MiscTests(SimpleTestCase):

    def setUp(self):
        super(MiscTests, self).setUp()
        self.rf = RequestFactory()

    @override_settings(LANGUAGE_CODE='de')
    def test_english_fallback(self):
        """
        With a non-English LANGUAGE_CODE and if the active language is English
        or one of its variants, the untranslated string should be returned
        (instead of falling back to LANGUAGE_CODE) (See #24413).
        """
        self.assertEqual(ugettext("Image"), "Bild")
        with translation.override('en'):
            self.assertEqual(ugettext("Image"), "Image")
        with translation.override('en-us'):
            self.assertEqual(ugettext("Image"), "Image")
        with translation.override('en-ca'):
            self.assertEqual(ugettext("Image"), "Image")

    def test_parse_spec_http_header(self):
        """
        Testing HTTP header parsing. First, we test that we can parse the
        values according to the spec (and that we extract all the pieces in
        the right order).
        """
        p = trans_real.parse_accept_lang_header
        # Good headers.
        self.assertEqual([('de', 1.0)], p('de'))
        self.assertEqual([('en-au', 1.0)], p('en-AU'))
        self.assertEqual([('es-419', 1.0)], p('es-419'))
        self.assertEqual([('*', 1.0)], p('*;q=1.00'))
        self.assertEqual([('en-au', 0.123)], p('en-AU;q=0.123'))
        self.assertEqual([('en-au', 0.5)], p('en-au;q=0.5'))
        self.assertEqual([('en-au', 1.0)], p('en-au;q=1.0'))
        self.assertEqual([('da', 1.0), ('en', 0.5), ('en-gb', 0.25)], p('da, en-gb;q=0.25, en;q=0.5'))
        self.assertEqual([('en-au-xx', 1.0)], p('en-au-xx'))
        self.assertEqual(
            [('de', 1.0), ('en-au', 0.75), ('en-us', 0.5), ('en', 0.25), ('es', 0.125), ('fa', 0.125)],
            p('de,en-au;q=0.75,en-us;q=0.5,en;q=0.25,es;q=0.125,fa;q=0.125')
        )
        self.assertEqual([('*', 1.0)], p('*'))
        self.assertEqual([('de', 0.0)], p('de;q=0.'))
        self.assertEqual([('en', 1.0), ('*', 0.5)], p('en; q=1.0, * ; q=0.5'))
        self.assertEqual([('en', 1.0)], p('en; q=1,'))
        self.assertEqual([], p(''))

        # Bad headers; should always return [].
        self.assertEqual([], p('en-gb;q=1.0000'))
        self.assertEqual([], p('en;q=0.1234'))
        self.assertEqual([], p('en;q=.2'))
        self.assertEqual([], p('abcdefghi-au'))
        self.assertEqual([], p('**'))
        self.assertEqual([], p('en,,gb'))
        self.assertEqual([], p('en-au;q=0.1.0'))
        self.assertEqual(
            [],
            p('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXZ,en')
        )
        self.assertEqual([], p('da, en-gb;q=0.8, en;q=0.7,#'))
        self.assertEqual([], p('de;q=2.0'))
        self.assertEqual([], p('de;q=0.a'))
        self.assertEqual([], p('12-345'))
        self.assertEqual([], p(''))
        self.assertEqual([], p('en;q=1e0'))

    def test_parse_literal_http_header(self):
        """
        Now test that we parse a literal HTTP header correctly.
        """
        g = get_language_from_request
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'pt-br'}
        self.assertEqual('pt-br', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'pt'}
        self.assertEqual('pt', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'es,de'}
        self.assertEqual('es', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'es-ar,de'}
        self.assertEqual('es-ar', g(r))

        # This test assumes there won't be a Django translation to a US
        # variation of the Spanish language, a safe assumption. When the
        # user sets it as the preferred language, the main 'es'
        # translation should be selected instead.
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'es-us'}
        self.assertEqual(g(r), 'es')

        # This tests the following scenario: there isn't a main language (zh)
        # translation of Django but there is a translation to variation (zh-hans)
        # the user sets zh-hans as the preferred language, it should be selected
        # by Django without falling back nor ignoring it.
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'zh-hans,de'}
        self.assertEqual(g(r), 'zh-hans')

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'NL'}
        self.assertEqual('nl', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'fy'}
        self.assertEqual('fy', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'ia'}
        self.assertEqual('ia', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'sr-latn'}
        self.assertEqual('sr-latn', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'zh-hans'}
        self.assertEqual('zh-hans', g(r))

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'zh-hant'}
        self.assertEqual('zh-hant', g(r))

    @override_settings(
        LANGUAGES=[
            ('en', 'English'),
            ('zh-hans', 'Simplified Chinese'),
            ('zh-hant', 'Traditional Chinese'),
        ]
    )
    def test_support_for_deprecated_chinese_language_codes(self):
        """
        Some browsers (Firefox, IE, etc.) use deprecated language codes. As these
        language codes will be removed in Django 1.9, these will be incorrectly
        matched. For example zh-tw (traditional) will be interpreted as zh-hans
        (simplified), which is wrong. So we should also accept these deprecated
        language codes.

        refs #18419 -- this is explicitly for browser compatibility
        """
        g = get_language_from_request
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'zh-cn,en'}
        self.assertEqual(g(r), 'zh-hans')

        r.META = {'HTTP_ACCEPT_LANGUAGE': 'zh-tw,en'}
        self.assertEqual(g(r), 'zh-hant')

    def test_special_fallback_language(self):
        """
        Some languages may have special fallbacks that don't follow the simple
        'fr-ca' -> 'fr' logic (notably Chinese codes).
        """
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'zh-my,en'}
        self.assertEqual(get_language_from_request(r), 'zh-hans')

    def test_parse_language_cookie(self):
        """
        Now test that we parse language preferences stored in a cookie correctly.
        """
        g = get_language_from_request
        r = self.rf.get('/')
        r.COOKIES = {settings.LANGUAGE_COOKIE_NAME: 'pt-br'}
        r.META = {}
        self.assertEqual('pt-br', g(r))

        r.COOKIES = {settings.LANGUAGE_COOKIE_NAME: 'pt'}
        r.META = {}
        self.assertEqual('pt', g(r))

        r.COOKIES = {settings.LANGUAGE_COOKIE_NAME: 'es'}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'de'}
        self.assertEqual('es', g(r))

        # This test assumes there won't be a Django translation to a US
        # variation of the Spanish language, a safe assumption. When the
        # user sets it as the preferred language, the main 'es'
        # translation should be selected instead.
        r.COOKIES = {settings.LANGUAGE_COOKIE_NAME: 'es-us'}
        r.META = {}
        self.assertEqual(g(r), 'es')

        # This tests the following scenario: there isn't a main language (zh)
        # translation of Django but there is a translation to variation (zh-hans)
        # the user sets zh-hans as the preferred language, it should be selected
        # by Django without falling back nor ignoring it.
        r.COOKIES = {settings.LANGUAGE_COOKIE_NAME: 'zh-hans'}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'de'}
        self.assertEqual(g(r), 'zh-hans')

    def test_get_language_from_path_real(self):
        g = trans_real.get_language_from_path
        self.assertEqual(g('/pl/'), 'pl')
        self.assertEqual(g('/pl'), 'pl')
        self.assertIsNone(g('/xyz/'))

    def test_get_language_from_path_null(self):
        from django.utils.translation.trans_null import get_language_from_path as g
        self.assertIsNone(g('/pl/'))
        self.assertIsNone(g('/pl'))
        self.assertIsNone(g('/xyz/'))

    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_percent_in_translatable_block(self):
        t_sing = Template("{% load i18n %}{% blocktrans %}The result was {{ percent }}%{% endblocktrans %}")
        t_plur = Template(
            "{% load i18n %}{% blocktrans count num as number %}"
            "{{ percent }}% represents {{ num }} object{% plural %}"
            "{{ percent }}% represents {{ num }} objects{% endblocktrans %}"
        )
        with translation.override('de'):
            self.assertEqual(t_sing.render(Context({'percent': 42})), 'Das Ergebnis war 42%')
            self.assertEqual(t_plur.render(Context({'percent': 42, 'num': 1})), '42% stellt 1 Objekt dar')
            self.assertEqual(t_plur.render(Context({'percent': 42, 'num': 4})), '42% stellt 4 Objekte dar')

    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_percent_formatting_in_blocktrans(self):
        """
        Test that using Python's %-formatting is properly escaped in blocktrans,
        singular or plural
        """
        t_sing = Template("{% load i18n %}{% blocktrans %}There are %(num_comments)s comments{% endblocktrans %}")
        t_plur = Template(
            "{% load i18n %}{% blocktrans count num as number %}"
            "%(percent)s% represents {{ num }} object{% plural %}"
            "%(percent)s% represents {{ num }} objects{% endblocktrans %}"
        )
        with translation.override('de'):
            # Strings won't get translated as they don't match after escaping %
            self.assertEqual(t_sing.render(Context({'num_comments': 42})), 'There are %(num_comments)s comments')
            self.assertEqual(t_plur.render(Context({'percent': 42, 'num': 1})), '%(percent)s% represents 1 object')
            self.assertEqual(t_plur.render(Context({'percent': 42, 'num': 4})), '%(percent)s% represents 4 objects')

    def test_cache_resetting(self):
        """
        #14170 after setting LANGUAGE, cache should be cleared and languages
        previously valid should not be used.
        """
        g = get_language_from_request
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'pt-br'}
        self.assertEqual('pt-br', g(r))
        with self.settings(LANGUAGES=[('en', 'English')]):
            self.assertNotEqual('pt-br', g(r))

    def test_i18n_patterns_returns_list(self):
        with override_settings(USE_I18N=False):
            self.assertIsInstance(i18n_patterns([]), list)
        with override_settings(USE_I18N=True):
            self.assertIsInstance(i18n_patterns([]), list)


class ResolutionOrderI18NTests(SimpleTestCase):

    def setUp(self):
        super(ResolutionOrderI18NTests, self).setUp()
        activate('de')

    def tearDown(self):
        deactivate()
        super(ResolutionOrderI18NTests, self).tearDown()

    def assertUgettext(self, msgid, msgstr):
        result = ugettext(msgid)
        self.assertIn(
            msgstr, result,
            "The string '%s' isn't in the translation of '%s'; the actual result is '%s'."
            % (msgstr, msgid, result)
        )


class AppResolutionOrderI18NTests(ResolutionOrderI18NTests):

    @override_settings(LANGUAGE_CODE='de')
    def test_app_translation(self):
        # Original translation.
        self.assertUgettext('Date/time', 'Datum/Zeit')

        # Different translation.
        with self.modify_settings(INSTALLED_APPS={'append': 'i18n.resolution'}):
            # Force refreshing translations.
            activate('de')

            # Doesn't work because it's added later in the list.
            self.assertUgettext('Date/time', 'Datum/Zeit')

            with self.modify_settings(INSTALLED_APPS={'remove': 'django.contrib.admin.apps.SimpleAdminConfig'}):
                # Force refreshing translations.
                activate('de')

                # Unless the original is removed from the list.
                self.assertUgettext('Date/time', 'Datum/Zeit (APP)')


@override_settings(LOCALE_PATHS=extended_locale_paths)
class LocalePathsResolutionOrderI18NTests(ResolutionOrderI18NTests):

    def test_locale_paths_translation(self):
        self.assertUgettext('Time', 'LOCALE_PATHS')

    def test_locale_paths_override_app_translation(self):
        with self.settings(INSTALLED_APPS=['i18n.resolution']):
            self.assertUgettext('Time', 'LOCALE_PATHS')


class DjangoFallbackResolutionOrderI18NTests(ResolutionOrderI18NTests):

    def test_django_fallback(self):
        self.assertEqual(ugettext('Date/time'), 'Datum/Zeit')


class TestModels(TestCase):
    def test_lazy(self):
        tm = TestModel()
        tm.save()

    def test_safestr(self):
        c = Company(cents_paid=12, products_delivered=1)
        c.name = SafeText('Iñtërnâtiônàlizætiøn1')
        c.save()
        c.name = SafeBytes('Iñtërnâtiônàlizætiøn1'.encode('utf-8'))
        c.save()


class TestLanguageInfo(SimpleTestCase):
    def test_localized_language_info(self):
        li = get_language_info('de')
        self.assertEqual(li['code'], 'de')
        self.assertEqual(li['name_local'], 'Deutsch')
        self.assertEqual(li['name'], 'German')
        self.assertIs(li['bidi'], False)

    def test_unknown_language_code(self):
        six.assertRaisesRegex(self, KeyError, r"Unknown language code xx\.", get_language_info, 'xx')
        with translation.override('xx'):
            # A language with no translation catalogs should fallback to the
            # untranslated string.
            self.assertEqual(ugettext("Title"), "Title")

    def test_unknown_only_country_code(self):
        li = get_language_info('de-xx')
        self.assertEqual(li['code'], 'de')
        self.assertEqual(li['name_local'], 'Deutsch')
        self.assertEqual(li['name'], 'German')
        self.assertIs(li['bidi'], False)

    def test_unknown_language_code_and_country_code(self):
        six.assertRaisesRegex(self, KeyError, r"Unknown language code xx-xx and xx\.", get_language_info, 'xx-xx')

    def test_fallback_language_code(self):
        """
        get_language_info return the first fallback language info if the lang_info
        struct does not contain the 'name' key.
        """
        li = get_language_info('zh-my')
        self.assertEqual(li['code'], 'zh-hans')
        li = get_language_info('zh-hans')
        self.assertEqual(li['code'], 'zh-hans')


class MultipleLocaleActivationTests(SimpleTestCase):
    """
    Tests for template rendering behavior when multiple locales are activated
    during the lifetime of the same process.
    """
    def setUp(self):
        super(MultipleLocaleActivationTests, self).setUp()
        self._old_language = get_language()

    def tearDown(self):
        super(MultipleLocaleActivationTests, self).tearDown()
        activate(self._old_language)

    def test_single_locale_activation(self):
        """
        Simple baseline behavior with one locale for all the supported i18n constructs.
        """
        with translation.override('fr'):
            self.assertEqual(Template("{{ _('Yes') }}").render(Context({})), 'Oui')
            self.assertEqual(Template("{% load i18n %}{% trans 'Yes' %}").render(Context({})), 'Oui')
            self.assertEqual(
                Template("{% load i18n %}{% blocktrans %}Yes{% endblocktrans %}").render(Context({})),
                'Oui'
            )

    # Literal marked up with _() in a filter expression

    def test_multiple_locale_filter(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{{ 0|yesno:_('yes,no,maybe') }}")
        with translation.override(self._old_language), translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'nee')

    def test_multiple_locale_filter_deactivate(self):
        with translation.override('de', deactivate=True):
            t = Template("{% load i18n %}{{ 0|yesno:_('yes,no,maybe') }}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'nee')

    def test_multiple_locale_filter_direct_switch(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{{ 0|yesno:_('yes,no,maybe') }}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'nee')

    # Literal marked up with _()

    def test_multiple_locale(self):
        with translation.override('de'):
            t = Template("{{ _('No') }}")
        with translation.override(self._old_language), translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_deactivate(self):
        with translation.override('de', deactivate=True):
            t = Template("{{ _('No') }}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_direct_switch(self):
        with translation.override('de'):
            t = Template("{{ _('No') }}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    # Literal marked up with _(), loading the i18n template tag library

    def test_multiple_locale_loadi18n(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{{ _('No') }}")
        with translation.override(self._old_language), translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_loadi18n_deactivate(self):
        with translation.override('de', deactivate=True):
            t = Template("{% load i18n %}{{ _('No') }}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_loadi18n_direct_switch(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{{ _('No') }}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    # trans i18n tag

    def test_multiple_locale_trans(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{% trans 'No' %}")
        with translation.override(self._old_language), translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_deactivate_trans(self):
        with translation.override('de', deactivate=True):
            t = Template("{% load i18n %}{% trans 'No' %}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_direct_switch_trans(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{% trans 'No' %}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    # blocktrans i18n tag

    def test_multiple_locale_btrans(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{% blocktrans %}No{% endblocktrans %}")
        with translation.override(self._old_language), translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_deactivate_btrans(self):
        with translation.override('de', deactivate=True):
            t = Template("{% load i18n %}{% blocktrans %}No{% endblocktrans %}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')

    def test_multiple_locale_direct_switch_btrans(self):
        with translation.override('de'):
            t = Template("{% load i18n %}{% blocktrans %}No{% endblocktrans %}")
        with translation.override('nl'):
            self.assertEqual(t.render(Context({})), 'Nee')


@override_settings(
    USE_I18N=True,
    LANGUAGES=[
        ('en', 'English'),
        ('fr', 'French'),
    ],
    MIDDLEWARE=[
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
    ROOT_URLCONF='i18n.urls',
)
class LocaleMiddlewareTests(TestCase):

    def test_streaming_response(self):
        # Regression test for #5241
        response = self.client.get('/fr/streaming/')
        self.assertContains(response, "Oui/Non")
        response = self.client.get('/en/streaming/')
        self.assertContains(response, "Yes/No")

    @override_settings(
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
        ],
    )
    def test_language_not_saved_to_session(self):
        """Checks that current language is not automatically saved to
        session on every request."""
        # Regression test for #21473
        self.client.get('/fr/simple/')
        self.assertNotIn(LANGUAGE_SESSION_KEY, self.client.session)


@override_settings(
    USE_I18N=True,
    LANGUAGES=[
        ('en', 'English'),
        ('fr', 'French'),
    ],
    MIDDLEWARE=[
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
    ROOT_URLCONF='i18n.urls_default_unprefixed',
    LANGUAGE_CODE='en',
)
class UnprefixedDefaultLanguageTests(SimpleTestCase):
    def test_default_lang_without_prefix(self):
        """
        With i18n_patterns(..., prefix_default_language=False), the default
        language (settings.LANGUAGE_CODE) should be accessible without a prefix.
        """
        response = self.client.get('/simple/')
        self.assertEqual(response.content, b'Yes')

    def test_other_lang_with_prefix(self):
        response = self.client.get('/fr/simple/')
        self.assertEqual(response.content, b'Oui')

    def test_unprefixed_language_other_than_accept_language(self):
        response = self.client.get('/simple/', HTTP_ACCEPT_LANGUAGE='fr')
        self.assertEqual(response.content, b'Yes')

    def test_unexpected_kwarg_to_i18n_patterns(self):
        with self.assertRaisesMessage(AssertionError, "Unexpected kwargs for i18n_patterns(): {'foo':"):
            i18n_patterns(object(), foo='bar')


@override_settings(
    USE_I18N=True,
    LANGUAGES=[
        ('bg', 'Bulgarian'),
        ('en-us', 'English'),
        ('pt-br', 'Portuguese (Brazil)'),
    ],
    MIDDLEWARE=[
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
    ROOT_URLCONF='i18n.urls'
)
class CountrySpecificLanguageTests(SimpleTestCase):

    def setUp(self):
        super(CountrySpecificLanguageTests, self).setUp()
        self.rf = RequestFactory()

    def test_check_for_language(self):
        self.assertTrue(check_for_language('en'))
        self.assertTrue(check_for_language('en-us'))
        self.assertTrue(check_for_language('en-US'))
        self.assertTrue(check_for_language('be'))
        self.assertTrue(check_for_language('be@latin'))
        self.assertTrue(check_for_language('sr-RS@latin'))
        self.assertTrue(check_for_language('sr-RS@12345'))
        self.assertFalse(check_for_language('en-ü'))
        self.assertFalse(check_for_language('en\x00'))
        self.assertFalse(check_for_language(None))
        self.assertFalse(check_for_language('be@ '))
        # Specifying encoding is not supported (Django enforces UTF-8)
        self.assertFalse(check_for_language('tr-TR.UTF-8'))
        self.assertFalse(check_for_language('tr-TR.UTF8'))
        self.assertFalse(check_for_language('de-DE.utf-8'))

    def test_get_language_from_request(self):
        # issue 19919
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.8,bg;q=0.6,ru;q=0.4'}
        lang = get_language_from_request(r)
        self.assertEqual('en-us', lang)
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'bg-bg,en-US;q=0.8,en;q=0.6,ru;q=0.4'}
        lang = get_language_from_request(r)
        self.assertEqual('bg', lang)

    def test_specific_language_codes(self):
        # issue 11915
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'pt,en-US;q=0.8,en;q=0.6,ru;q=0.4'}
        lang = get_language_from_request(r)
        self.assertEqual('pt-br', lang)
        r = self.rf.get('/')
        r.COOKIES = {}
        r.META = {'HTTP_ACCEPT_LANGUAGE': 'pt-pt,en-US;q=0.8,en;q=0.6,ru;q=0.4'}
        lang = get_language_from_request(r)
        self.assertEqual('pt-br', lang)


class TranslationFilesMissing(SimpleTestCase):

    def setUp(self):
        super(TranslationFilesMissing, self).setUp()
        self.gettext_find_builtin = gettext_module.find

    def tearDown(self):
        gettext_module.find = self.gettext_find_builtin
        super(TranslationFilesMissing, self).tearDown()

    def patchGettextFind(self):
        gettext_module.find = lambda *args, **kw: None

    def test_failure_finding_default_mo_files(self):
        '''
        Ensure IOError is raised if the default language is unparseable.
        Refs: #18192
        '''
        self.patchGettextFind()
        trans_real._translations = {}
        with self.assertRaises(IOError):
            activate('en')


class NonDjangoLanguageTests(SimpleTestCase):
    """
    A language non present in default Django languages can still be
    installed/used by a Django project.
    """
    @override_settings(
        USE_I18N=True,
        LANGUAGES=[
            ('en-us', 'English'),
            ('xxx', 'Somelanguage'),
        ],
        LANGUAGE_CODE='xxx',
        LOCALE_PATHS=[os.path.join(here, 'commands', 'locale')],
    )
    def test_non_django_language(self):
        self.assertEqual(get_language(), 'xxx')
        self.assertEqual(ugettext("year"), "reay")

    @override_settings(
        USE_I18N=True,
        LANGUAGES=[
            ('en-us', 'English'),
            # xyz language has no locale files
            ('xyz', 'XYZ'),
        ],
    )
    @translation.override('xyz')
    def test_plural_non_django_language(self):
        self.assertEqual(get_language(), 'xyz')
        self.assertEqual(ungettext('year', 'years', 2), 'years')

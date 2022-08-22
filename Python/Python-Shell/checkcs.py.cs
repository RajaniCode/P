class Iterators
{
    public IEnumerator GetEnumerator()
    {   
        //Less than 100
        for (int i = 0; i < 100; i++)
        {
            //Less than 20
            if (i == 20) yield break;
            {    
                //Even Number
                if (i % 2 == 0)
                {
                    yield return i;
                }
            }
        }
    }

    public IEnumerable Power(int number, int exponent)
    {
        int count = 0;
        int result = 1;
        while (count++ < exponent)
        {
            //if (count == 3) yield break; //Up to Square
            result *= number;
            yield return result;

        }
    }
}

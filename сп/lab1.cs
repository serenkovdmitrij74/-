using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        string s = "abbccacdaeb";
        HashSet<string> results = new HashSet<string>();

        for (int i = 0; i < s.Length; i++)
        {
            for (int j = i; j < s.Length; j++)
            {
                string sub = s.Substring(i, j - i + 1);

                if (Matches(sub))
                {
                    results.Add(sub);
                }
            }
        }

        Console.WriteLine("Подходящие фрагменты:");

        foreach (string sub in results)
        {
            Console.WriteLine(sub);
        }
    }

    static bool Matches(string s)
    {
        int i = 0;

        while (i < s.Length)
        {
            while (i < s.Length && (s[i] == 'a' || s[i] == 'b'))
            {
                i++;
            }

            if (i >= s.Length || s[i] != 'c')
                return false;

            while (i < s.Length && s[i] == 'c')
            {
                i++;
            }
        }

        return s.Length > 0;
    }
}
#include <stdio.h>

int main ()
{
   int i = 100000;
   int j = 555;

   if (i > j){
       int aux = j;
       j = i;
       i = aux;
   }

   int r = 0;
   int count = 1;

    for(int bit=0;bit<(sizeof(j)*8); bit++)
   {

        if ((j & 0x01) == 1){
            r += count * i;
        }

        count *= 2;
        j = j >> 1;
   }

   printf("%i\n", r);
   return 0;
}
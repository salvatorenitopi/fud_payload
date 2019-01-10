#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void XorBuffer(char * buffer1, char * buffer2, int len, char * dest)
{
  int i;
  for(i = 0; i < len; i++)
  {
    dest[i] = buffer1[i] ^ buffer2[i];
  }
}

int main(void)
{
  char dest[6];
  char lol[6];
  XorBuffer("123456", "123450", 6, dest);
  printf("%s", dest);

  XorBuffer(dest, "123450", 6, lol);
  printf("%s", lol);

}
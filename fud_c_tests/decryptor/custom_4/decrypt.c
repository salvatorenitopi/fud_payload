#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void print_hex(const char *s)
{
	while(*s)
		printf("%02x:", (unsigned int) *s++);
	printf("\n");
}

void derandomize (const char *in_buf, char *out_buf, int junk){
	
	int len = (size_t)strlen(in_buf);

	int pos = 0;
	int counter = 0;
	for (int i=0; i<len; i++){
		counter += 1;
		if ( (counter % (junk + 1)) == 0 ){
			out_buf[pos] = in_buf[i];
			pos += 1;
		}
	}

}

int main (){
	char out[34] = {};
	char buff[] = 
	"WQEFCkUkmiAmgBaDpdSoO5ud AmX1c4pXYo37cBmkCO9efd8T 1mhSvCBcaa8BvC"
	"?BVUL RQhBIcajGoHmN1 uWkZtxtMru9fgBtvslrtuEdioJzkg qWfKbLSWbesXV"
	"HnS5sXeayVZ 0HwreXfvA v88XtIJD3uRfEU?";

	derandomize (buff, out, 4);

	printf ("\n\n%s", out);

	int len = (size_t)strlen(out);
	printf ("\n\n%d\n\n", len);
}










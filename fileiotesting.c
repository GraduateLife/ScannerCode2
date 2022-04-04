#include <stdio.h>
#include <string.h>
#include <stdint.h>
//commenting dlexport to compile on mac
//__declspec(dllexport)
void write_to_csv(char *filename,int16_t a[],int n);
//parameters are filepointer, 2d array, n by m dimensions 
void write_to_csv(char *filename,int16_t a[],int n){
FILE *fp;
int i,j;
 
    
filename=strcat(filename,".csv");
fp=fopen(filename,"w+");


for(i=0;i<n;i++){
    if(i == (n-1)){
        fprintf(fp,"%u \n",(unsigned int)a[i]);
    }
    else{
        fprintf(fp,"%u,",(unsigned int)a[i]);
    }
    //fprintf(fp,"\n%d",i+1);
 
 
 
    }
 
fclose(fp);
 
//printf("\n %s file created",filename);
 
}
/*
int main(){
 
    int a[3][3]={{50,50,50},{60,60,60},{70,70,70}};
 

    
    char str[] = "picoValues";
 
create_marks_csv(str,a,3,3);
 
return 0;
 
}
*/
//Example for sending TMCL commands as datagrams to a module.
//The functions for handling the serial port must be added by the user.

//Data types used here: UCHAR: 1 byte (unsigned char)
//                      INT:   4 byte integer ("long" on most MCUs)


//Opcodes of all TMCL commands that can be used in direct mode
//type seems to be some sort of conditional that the mcu uses


#include<windows.h>
#include<stdio.h>
#include <time.h>

#define TMCL_ROR 1
#define TMCL_ROL 2
#define TMCL_MST 3
#define TMCL_MVP 4
#define TMCL_SAP 5
#define TMCL_GAP 6
#define TMCL_STAP 7
#define TMCL_RSAP 9
#define TMCL_SGP 9
#define TMCL_GGP 10
#define TMCL_STGP 11
#define TMCL_RSGP 12
#define TMCL_RFS 13
#define TMCL_SIO 14
#define TMCL_GIO 15
#define TMCL_SCO 30
#define TMCL_GCO 31
#define TMCL_CCO 32

//Opcodes of TMCL control functions (to be used to run or abort a TMCL program in the module)
#define TMCL_APPL_STOP 128
#define TMCL_APPL_RUN 129
#define TMCL_APPL_RESET 131

//Options for MVP commandds
#define MVP_ABS 0
#define MVP_REL 1
#define MVP_COORD 2

//Options for RFS command
#define RFS_START 0
#define RFS_STOP 1
#define RFS_STATUS 2

#define FALSE 0
#define TRUE 1


//global variables
HANDLE hComm;

  //X Axis Com ports
HANDLE hComm2;


HANDLE hComm3;


void SendCmd(HANDLE comport,UCHAR Address, UCHAR Command, UCHAR Type, UCHAR Motor, INT Value);
UCHAR GetResult(HANDLE Handle, UCHAR *Address, UCHAR *Status, INT *Value);
void openhComm(char comstring[]);
void openhComm2(char comstring[]);
void openhComm3(char comstring[]);
void checkMotorPower();
__declspec(dllexport)int YAxismoveToPositionN(INT Position);
__declspec(dllexport)int XAxismoveToPositionN(INT Position);
__declspec(dllexport)void openSerialPorts(char comString1[],char comstring2[],char comstring3[]);
__declspec(dllexport)void closeSerialPorts();
__declspec(dllexport)int motorSetup(INT motorSpeed);
__declspec(dllexport)void checkMotorAssignment();

void delay(int number_of_seconds)
{
    // Converting time into milli_seconds
    int milli_seconds = 1000 * number_of_seconds;
  
    // Storing start time
    clock_t start_time = clock();
  
    // looping till required time is not achieved
    while (clock() < start_time + milli_seconds)
        ;
}

// int main(){
	
// 	openSerialPorts("\\\\.\\COM3","\\\\.\\COM4","\\\\.\\COM5");
// 	motorSetup();
// 	XAxismoveToPositionN(5000);
// 	YAxismoveToPositionN(20000);
// 	closeSerialPorts();
	
// 	printf("Hello World \n");
// }


void closeSerialPorts(){
	CloseHandle(hComm);
  	CloseHandle(hComm2);
  	CloseHandle(hComm3);
}


void checkMotorPower(){
	UCHAR Address = 0x01;
	UCHAR Type, Motor,Status = 0x00;
	INT Value1 = 0;
	INT Value2 = 0;
	INT Value3 = 0;
	INT Position1 = 1;
	printf("Moving to position %d \n",Position1);
	SendCmd(hComm,Address,TMCL_MVP,0x00,0x00,Position1);
	GetResult(hComm,&Address,&Status,&Value1);
	if(Status == 6){
		SendCmd(hComm,Address,TMCL_GGP,0x42,0x00,0);
		GetResult(hComm,&Address,&Status,&Value1);
		printf("Issue with motor power on motor id %d, do not proceed \n",Value1);
	}
	SendCmd(hComm2,Address,TMCL_MVP,0x00,0x00,Position1);
	GetResult(hComm2,&Address,&Status,&Value2);
	if(Status == 6){
		SendCmd(hComm,Address,TMCL_GGP,0x42,0x00,0);
		GetResult(hComm,&Address,&Status,&Value2);
		printf("Issue with motor power on motor id %d, do not proceed \n",Value2);
	}
	SendCmd(hComm3,Address,TMCL_MVP,0x00,0x00,Position1);
	GetResult(hComm3,&Address,&Status,&Value3);
	if(Status == 6){
		SendCmd(hComm,Address,TMCL_GGP,0x42,0x00,0);
		GetResult(hComm,&Address,&Status,&Value3);
		printf("Issue with motor power on motor id %d, do not proceed \n",Value2);
	}
}


void checkMotorAssignment(){
	UCHAR Address = 0x01;
 	UCHAR Type, Motor,Status = 0x00;
 	INT Value = 0;
	SendCmd(hComm3,Address,TMCL_GGP,0x42,0x00,0);
	GetResult(hComm3,&Address,&Status,&Value);
	printf("Value returned by hcomm3 is %d \n",Value);
	if(Value != 2){
		printf("Something has gone terribly wrong with motor assignment \n");
	}
}

void openhComm(char comstring[]){
	
	hComm = CreateFileA(comstring,                //port name
                      GENERIC_READ | GENERIC_WRITE, //Read/Write
                      0,                            // No Sharing
                      NULL,                         // No Security
                      OPEN_EXISTING,// Open existing port only
                      0,            // Non Overlapped I/O
                      NULL);        // Null for Comm Devices

  if (hComm == INVALID_HANDLE_VALUE)
      printf("Error in opening serial port hcomm \n");
  else
      printf("opening serial port hcomm successful \n");
}

void openhComm2(char comstring[]){
	hComm2 = CreateFileA(comstring,                //port name
                      GENERIC_READ | GENERIC_WRITE, //Read/Write
                      0,                            // No Sharing
                      NULL,                         // No Security
                      OPEN_EXISTING,// Open existing port only
                      0,            // Non Overlapped I/O
                      NULL);        // Null for Comm Devices

  if (hComm2 == INVALID_HANDLE_VALUE)
      printf("Error in opening serial port hcomm2 \n");
  else
      printf("opening serial port hcomm2 successful \n");
}

void openhComm3(char comstring[]){
	hComm3 = CreateFileA(comstring,                //port name
                      GENERIC_READ | GENERIC_WRITE, //Read/Write
                      0,                            // No Sharing
                      NULL,                         // No Security
                      OPEN_EXISTING,// Open existing port only
                      0,            // Non Overlapped I/O
                      NULL);        // Null for Comm Devices

  if (hComm3 == INVALID_HANDLE_VALUE)
      printf("Error in opening serial port hcomm3 \n");
  else
      printf("opening serial port hcomm3 successful \n");
}




void openSerialPorts(char comstring1[],char comstring2[],char comstring3[]){
	
	UCHAR Address = 0x01;
 	UCHAR Type, Motor,Status = 0x00;
 	INT Value = 0;
	printf("Comstring1 is %s \n",comstring1);
	
	openhComm(comstring1);

	SendCmd(hComm,Address,TMCL_GGP,0x42,0x00,0);
	GetResult(hComm,&Address,&Status,&Value);
	printf("Value returned by hcomm is %d \n",Value);

	if(Value == 2){
		printf("X motor found, closing hComm, opening hComm3 \n");
		CloseHandle(hComm);
		openhComm3(comstring1);
		openhComm2(comstring2);
		openhComm(comstring3);
	}


	else{
		openhComm2(comstring2);
		SendCmd(hComm2,Address,TMCL_GGP,0x42,0x00,0);
		GetResult(hComm2,&Address,&Status,&Value);
		printf("Value returned by hcomm2 is %d \n",Value);
		if(Value == 2){
			printf("X motor found, closing hComm2, opening hComm3 \n");
			CloseHandle(hComm2);
			openhComm3(comstring2);
			openhComm2(comstring3);
	}

 
	else{
		openhComm3(comstring3);
	
	}
	}
	
}

int motorSetup(INT motorSpeed){
	UCHAR Address = 0x01;
 	UCHAR Type, Motor,Status = 0x00;
 	INT Value = 0;

SendCmd(hComm,Address,TMCL_SAP,0x9A,0x00,4);
GetResult(hComm,&Address,&Status,&Value);  //Set Pulse divisor
SendCmd(hComm2,Address,TMCL_SAP,0x9A,0x00,4);
GetResult(hComm2,&Address,&Status,&Value);
SendCmd(hComm3,Address,TMCL_SAP,0x9A,0x00,4);
GetResult(hComm3,&Address,&Status,&Value);


SendCmd(hComm,Address,TMCL_SAP,0x99,0x00,6);
GetResult(hComm,&Address,&Status,&Value); //Set Ramp divisor
SendCmd(hComm2,Address,TMCL_SAP,0x99,0x00,6);
GetResult(hComm2,&Address,&Status,&Value);
SendCmd(hComm3,Address,TMCL_SAP,0x99,0x00,6);
GetResult(hComm3,&Address,&Status,&Value);

SendCmd(hComm,Address,TMCL_SAP,0x8C,0x00,3);
GetResult(hComm,&Address,&Status,&Value);  //Set Microstep Resolution
SendCmd(hComm2,Address,TMCL_SAP,0x8C,0x00,3);
GetResult(hComm2,&Address,&Status,&Value);
SendCmd(hComm3,Address,TMCL_SAP,0x8C,0x00,3);
GetResult(hComm3,&Address,&Status,&Value);

SendCmd(hComm,Address,TMCL_SAP,0x04,0x00,motorSpeed);
GetResult(hComm,&Address,&Status,&Value);  //Set Maximum positioning speed
SendCmd(hComm2,Address,TMCL_SAP,0x04,0x00,motorSpeed);
GetResult(hComm2,&Address,&Status,&Value);
SendCmd(hComm3,Address,TMCL_SAP,0x04,0x00,motorSpeed);
GetResult(hComm3,&Address,&Status,&Value);

SendCmd(hComm,Address,TMCL_SAP,0x05,0x00,200);
GetResult(hComm,&Address,&Status,&Value);  //Set Maximum acceleration
SendCmd(hComm2,Address,TMCL_SAP,0x05,0x00,200);
GetResult(hComm2,&Address,&Status,&Value);
SendCmd(hComm3,Address,TMCL_SAP,0x05,0x00,200);
GetResult(hComm3,&Address,&Status,&Value);
if(XAxismoveToPositionN(1) == 1 && YAxismoveToPositionN(1)== 1){
	XAxismoveToPositionN(0);
	YAxismoveToPositionN(0);
	printf("Motor Check returning 1 \n");
	return 1;
}
else{
	return 0;
}

}


int YAxismoveToPositionN(INT Position){
	
	
	UCHAR Address = 0x01;
	UCHAR Type, Motor,Status = 0x00;
	INT Value1 = 0;
	INT Value2 = 0;
	printf("Moving to position %d \n",Position);
	SendCmd(hComm,Address,TMCL_MVP,0x00,0x00,Position);
	GetResult(hComm,&Address,&Status,&Value1);
	if(Status == 6){
		printf("Issue with motor power, do not proceed \n");
		return 0;
	}
	SendCmd(hComm2,Address,TMCL_MVP,0x00,0x00,Position);
	GetResult(hComm2,&Address,&Status,&Value2);
	if(Status == 6){
		printf("Issue with motor power, do not proceed \n");
		return 0;
	}
	SendCmd(hComm,Address,TMCL_GAP,0x08,0x00,0);
	GetResult(hComm,&Address,&Status,&Value1);
	SendCmd(hComm2,Address,TMCL_GAP,0x08,0x00,0);
	GetResult(hComm2,&Address,&Status,&Value2);
	
	

	while(Value1 != 1 && Value2 != 1 ){
		//printf("y motors looping to position %d \n",Position);
		SendCmd(hComm,Address,TMCL_GAP,0x08,0x00,0);
		GetResult(hComm,&Address,&Status,&Value1);
		SendCmd(hComm2,Address,TMCL_GAP,0x08,0x00,0);
		GetResult(hComm2,&Address,&Status,&Value2);
		
	
	}
	return 1;

}






int XAxismoveToPositionN(INT Position){
	
	printf("X Motors Moving to position %d \n", Position);
	UCHAR Address = 0x01;
	UCHAR Type, Motor,Status = 0x00;
	INT Value = 0;
	
	SendCmd(hComm3,Address,TMCL_MVP,0x00,0x00,Position);
	GetResult(hComm3,&Address,&Status,&Value);
	/*
	if(Status == 6){
		printf("Issue with motor power, do not proceed \n");
		return 0;
	*/
	
	SendCmd(hComm3,Address,TMCL_GAP,0x08,0x00,0);
	GetResult(hComm3,&Address,&Status,&Value);
	

	
	

	while(Value != 1){
		//printf("X motor Looping  to position %d\n",Position);
		SendCmd(hComm3,Address,TMCL_GAP,0x08,0x00,0);
		GetResult(hComm3,&Address,&Status,&Value);
		//printf("moving to desired position \n");
		

	}
	
	return 1;
	
}


//Send a command
void SendCmd(HANDLE comport, UCHAR Address, UCHAR Command, UCHAR Type, UCHAR Motor, INT Value)
{
	UCHAR TxBuffer[9];
	UCHAR i;

	TxBuffer[0]=Address;
	TxBuffer[1]=Command;
	TxBuffer[2]=Type;
	TxBuffer[3]=Motor;
	TxBuffer[4]=Value >> 24;
	TxBuffer[5]=Value >> 16;
	TxBuffer[6]=Value >> 8;
	TxBuffer[7]=Value & 0xff;
	TxBuffer[8]=0;
	for(i=0; i<8; i++)
		TxBuffer[8]+=TxBuffer[i];
	//Now, send the 9 bytes stored in TxBuffer to the module
  //(this is MCU specific) 
	BOOL Status = 0 ;
	Status = WriteFile(comport,TxBuffer,9, NULL,NULL);
	//printf("Write File Status is: %d \n",Status);

	
}




//Get the result
//Return TRUE when checksum of the result if okay, else return FALSE
// The follwing values are returned:
//      *Address: Host address
//      *Status: Status of the module (100 means okay)
//      *Value: Value read back by the command
UCHAR GetResult(HANDLE Handle, UCHAR *Address, UCHAR *Status, INT *Value)
{
	UCHAR RxBuffer[9], Checksum;
	DWORD Errors, BytesRead;
	COMSTAT ComStat;
	int i;
	

  //First, get 9 bytes from the module and store them in RxBuffer[0..8]
  //(this is MCU specific)
	BOOL ReadStatus = 0 ;
	ReadStatus = ReadFile(Handle,RxBuffer,9,NULL,NULL);
	//printf("Read File Status is: %d \n",ReadStatus);
	//Check the checksum
	Checksum=0;
	for(i=0; i<8; i++)
		//printf("%d \n",RxBuffer[i]);
		Checksum+=RxBuffer[i];

	//printf("checksum is %d, should be %d \n",Checksum,RxBuffer[8]);
	if(Checksum!=RxBuffer[8]){ 
		//printf("checksum returning false");
		return FALSE;
	}
	//printf("Status before assignment is %d \n",*Status);
	//Decode the datagram
	*Address=RxBuffer[0];
	*Status=RxBuffer[2];
	//printf("Status returned by Motor is %d \n",*Status);
	*Value=(RxBuffer[4] << 24) | (RxBuffer[5] << 16) | (RxBuffer[6] << 8) | RxBuffer[7];
	/*
	if (*Value == 6){
		printf("Motor Error - Likely Power");
	}
	*/
	return TRUE;
}

//analyze_mp3.cpp

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
//#include <conio.h>

#include "../../Software/Chord-Detector-and-Chromagram/src/Chromagram.h"
#include "../../Software/Chord-Detector-and-Chromagram/src/ChordDetector.h"

using namespace std;

int main(int argc, char **argv)
{
  if (argc < 2)
  {
    printf("No filename given. Exiting program.\n");
    exit(0);
  }

  string MP3_filename(argv[1]);

  printf("Analyzing '%s'.\n", MP3_filename.c_str());

  //Chromagram chromagram;
  //ChordDetector chord_detector;

  /**********************************************************************
  ** http://www.cplusplus.com/forum/general/105054/ **
  **********************************************************************/

	FILE* pFile;
	errno_t err;
	unsigned int uiFrame           = 0,
		check              = 0,
		test               = 0,
		CheckFlag          = 0,
		cntSize            = 0,
		uiFrameCount       = 1,
		PrevoiusFrameSize  = 0,
		TotalFileSize      = 0;

	int bitrate[16] = {0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0};
	int samp_freq[4]= {44, 48, 32, 0};

	if( 0 != (err  = fopen( &pFile, "C:\\test.mp3", "rb" )) ) {
		printf( "The input file was not opened\n" );
		return 1;
	}
	fseek(pFile, 0, SEEK_END);
	TotalFileSize = ftell(pFile);
	fseek(pFile, 0, SEEK_SET);

	while(cntSize < TotalFileSize/*10 > uiFrameCount*/)
	{
		// Check for the SynBits
		do
		{
			uiFrame = getc(pFile);
			if(EOF == uiFrame)
				break;
			cntSize++;
			if(0xFF == uiFrame)
			{
				uiFrame = getc(pFile);
				if(EOF == uiFrame)
					break;
				if((0xFA == uiFrame) || (0xFB == uiFrame))
				{
					if(1 != uiFrameCount)
						printf("\nFrame Size is %d \n\n",cntSize - PrevoiusFrameSize);

					printf("\nFrame Found at Byte %d", cntSize);
					PrevoiusFrameSize = cntSize;
					CheckFlag         = 1;
					uiFrameCount++;
				}
				cntSize++;
			}
		}while(1 != CheckFlag);

		CheckFlag = 0;

		//Check for MPEG Version
		check = uiFrame & 0x08;
		switch(check)
		{
		case  0x00:
			printf("\nError");
			break;
		case  0x08:
			printf("\nMPEG 1");
			break;
		}

		//Check for Layer
		check = uiFrame & 0x06;
		switch(check)
		{
		case  0x00:
			printf("\nReserved");
			break;
		case  0x02:
			printf("\nLayer 3");
			break;
		case  0x04:
			printf("\nLayer 2");
			break;
		case  0x06:
			printf("\nLayer 1");
			break;
		}

		//CRC Added or not
		test = uiFrame & 0x01;
		switch(test)
		{
		case  0x00:
			printf("\nRedundancy Added");
			break;
		case  0x01:
			printf("\nRedundancy Not Added");
			break;
		}

		// get next byte
		uiFrame = getc(pFile);
		if(uiFrame == EOF)
			break;
		cntSize++;

		// Check for Bit rate
		check = uiFrame & 0xF0;
		test = check >> 4;
		printf("\nBitrate is %d\n",bitrate[test]);

		// Check for Sampling Frequency
		check = uiFrame & 0x0C;
		test = check >> 2;
		printf("Sampling Frequency is %d\n",samp_freq[test]);

		// Check slot for bitrate change
		check = uiFrame& 0x02;
		switch(check)
		{
		case  0x00:
			printf("No Slot to adjust bit rate");
			break;
		case  0x02:
			printf("Slot to adjust bit rate");
			break;
		}

		// Check private bit
		check = uiFrame & 0x01;
		printf("\nPrivate Bit is %d\n", check);

		// Get next byte
		uiFrame = getc(pFile);
		if(uiFrame == EOF)
			break;
		cntSize++;
		// Check for channel type
		check = uiFrame & 0xC0;
		switch(check)
		{
		case  0x00:
			printf("Stereo");
			break;
		case  0x40:
			printf("Joint Stereo");
			break;
		case  0x80:
			printf("Dual Channel");
			break;
		case  0xC0:
			printf("Single Channel");
			break;
		}

		// Intensity and MS Stero Check
		check = uiFrame & 0x30;
		test = check >> 4;
		switch(test)
		{
		case  0x00:
			printf("\nIntensity Stereo-OFF MS Stereo-OFF");
			break;
		case  0x10:
			printf("\nIntensity Stereo-ON MS Stereo-OFF");
			break;
		case  0x20:
			printf("\nIntensity Stereo-OFF MS Stereo-ON");
			break;
		case  0x30:
			printf("\nIntensity Stereo-ON MS Stereo-ON");
			break;
		}

		// Check for Copyright
		check = uiFrame& 0x08;
		switch(check)
		{
		case  0x00:
			printf("\nNo Copyright");
			break;
		case  0x08:
			printf("\nCopyrighted");
			break;
		}

		// Check for Original or Copy
		check = uiFrame & 0x04;
		switch(check)
		{
		case  0x00:
			printf("\nCopy");
			break;
		case  0x04:
			printf("\nOriginal");
			break;
		}

		// Check for Emphasis
		check = uiFrame& 0x03;
		switch(check)
		{
		case  0:
			printf("\nNo Emphasis");
			break;
		case  1:
			printf("\n50/15 Micro seconds");
			break;
		case  2:
			printf("\nReserved");
			break;
		case  3:
			printf("\nCCITT J.17");
			break;
		}
		getch();
	}

	printf("\nTotal Number of Frames displayed is %d \n", uiFrameCount);
	fclose(pFile);
}

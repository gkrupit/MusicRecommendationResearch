//importMP3.h
/* some useful headers */
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>

//my headers
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>

using namespace std;

/* these values for bitrates and frequencies might come in useful */
unsigned int bitrate[] = {0,32000,40000,48000,56000,64000,80000,96000,112000,128000,160000,192000,224000,256000,320000,0};
unsigned int freq[]    = {44100,48000,32000,00000};

/* this is the function we're looking to call, with the values you have calculated */
void printmp3details(unsigned int nFrames, unsigned int nSampleRate, double fAveBitRate)
{
    printf("MP3 details:\n");
    printf("Frames: %d\n", nFrames);
    printf("Sample rate:%d\n", nSampleRate);
    printf("Ave bitrate:%0.0f\n", fAveBitRate);
}


//function to output sample frequency based on binary input
int calcsamprate(string inputbinary)
{
	if(inputbinary == "00")
		return(freq[0]);
	else if(inputbinary == "01")
		return(freq[1]);
	else if(inputbinary == "10")
		return(freq[2]);
	else
	{
		cerr << "incorrect sample frequency rate found in header" << endl;
		exit(1);
	}
}

//function to output bitrate of frame based on binary input
int calcbitrate(string inputbinary)
{
	if(inputbinary == "0000")
		return(freq[0]);
	if(inputbinary == "0001")
		return(freq[1]);
	if(inputbinary == "0010")
		return(freq[2]);
	if(inputbinary == "0011")
		return(freq[3]);
	if(inputbinary == "0100")
		return(freq[4]);
	if(inputbinary == "0101")
		return(freq[5]);
	if(inputbinary == "0110")
		return(freq[6]);
	if(inputbinary == "0111")
		return(freq[7]);
	if(inputbinary == "1000")
		return(freq[8]);
	if(inputbinary == "1001")
		return(freq[9]);
	if(inputbinary == "1010")
		return(freq[10]);
	if(inputbinary == "1011")
		return(freq[11]);
	if(inputbinary == "1100")
		return(freq[12]);
	if(inputbinary == "1101")
		return(freq[13]);
	if(inputbinary == "1110")
		return(freq[14]);
	if(inputbinary == "1111")
		return(freq[15]);
	else
	{
		cerr << "incorrect bitrate found in header" << endl;
		exit(1);
	}
}

void calculatedetails(ifstream & file)	//function taking inputfilestream as argument to calculate required information and call printmp3details
{
	file.seekg(0, ios::end);			// obtain filesize in bits
    size_t filesize = file.tellg();		//

    string mp3contents;					//create string and allocate correct amount of memory
    mp3contents.reserve(filesize);		//

	char * buffer;						//array of characters to transfer binary data prior to copying to string
	buffer = new char [filesize];		//dynamically allocate memory

	file.seekg(0, ios::beg);			//transfer binary data from file to buffer array
	file.read(buffer, filesize);		//
	file.close();						//

	int filebitsize = filesize *8;
	char * bitstorage;
	bitstorage = new char [filebitsize];

	for(unsigned int i = 0; i < filesize; i++)
	{
		for(int k = 0; k < 8; k++)
		{
			bitstorage[(i*8)+k] = (buffer[i] >> k) & 1; //convert from bytes to bits
		}
	}
	mp3contents.append(bitstorage);

	delete [] buffer;						//delete data from dynamically allocated memory
	delete [] bitstorage;

	vector<int> framepositions;			//vector to store location in string of all frames

	size_t searchpos = 0;
	string searchterm = "111111111111";
	int j = 0;
	while(mp3contents.find(searchterm, searchpos) != -1)			// while loop to find beginning of all frames in string and store their starting positions in vector
	{
		j++;
		framepositions.push_back(mp3contents.find(searchterm, searchpos));
		searchpos = framepositions[j] + 12;
	}

	string sampleratebinary = mp3contents.substr(framepositions[0] + 21, 2); //create substring containing sample rate info in binary

	int ongoingtotal = 0;
	for(unsigned int i = 0; i < framepositions.size(); i++)					// for loop to find all values of bitrate and add them all together
	{
		string bitratesubstr = mp3contents.substr(framepositions[i] + 17, 4);
		ongoingtotal = ongoingtotal + calcbitrate(bitratesubstr);
	}
	ongoingtotal = ongoingtotal/framepositions.size(); //averaging line

	printmp3details(framepositions.size(), calcsamprate(sampleratebinary), ongoingtotal);
}

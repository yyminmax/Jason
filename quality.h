/*




*/

#ifndef TRIM_H_
#define TRIM_H_

#include<string>
#include<vector>
#include<omp.h>
#include "zlib.h"

typedef vector<string*> vs;

using namespace std;

class TRIM 
{
    public:
        TRIM();
        TRIM(string name1, string name2);
        TRIM(string name);
        ~TRIM();
        vs * read_fq(string name);
        bool align(string seq, string adpter); 
        void quality_trim();
        void seq_stat();
    private:
        string name1;
        string name2;
        string name;
        string ttype;
};

TRIM::TRIM()
{
    this->name1 = "LM_SPE_R1.fq.gz";
    this->name2 = "LM_SPE_R2.fq.gz";
    this->ttype = "pair";
}

TRIM::TRIM(string name1, string name2)
{
    this->name1 = name1;
    this->name2 = name2;
    this->ttype = "pair";
}

TRIM::TRIM(string name)
{
    this->name = name;
    this->ttype = "single";
}

vs * TRIM::read_fq(string name)
{
    string * fq = new string[4];
    vs Fq(0);
    int count = 1;
    char pData[200];
    gzFile fData = gzopen(name, "rb");
    char * temp = gzgets(fData, pData, 200);
    fq[0] = temp;
    while(temp != "")
    {
        temp = gzgets(fData, pData, 200);
        fq[count++] = temp;
        if(count == 4)
        {
            Fq.push_back(fq);
            count = 0;
        }
    }
    gzclose(fData);
    return &Fq; 
}

bool TRIM::align(string seq, string adpter)
{

}

void TRIM::quality_trim()
{
    string adpter = "AGATCGGAAG";
    if( this->ttype == "pair" ) 
    {
        #pragma omp parallel sections
        {
            #pragma omp section
            vs * fq1 = this->read_fq(this->name1);
            #pragma omp section
            vs * fq2 = this->read_fq(this->name2);
        }
        #pragma omp parallel for num_threads(60)
        for(int i = 0; i < *fq1.size(); i++) 
        {
            if( this->align(*fq1[i][1], adpter) && this->align(*fq2[i][1], adpter) )
        }
    }
    else if( this->ttype == "single" )
    {
        vs * fq = this->read_fq(this->name);
    }
}

#endif 

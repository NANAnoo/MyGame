#include "gravity.h"
//#include <stdio.h>
//#include <stdlib.h>
//#include <time.h>
float InvSqrt(float x){
    float xhalf = 0.5f*x;
    int i = *(int*)&x; // get bits for floating VALUE
    i = 0x5f375a86- (i>>1); // gives initial guess y0
    x = *(float*)&i; // convert bits BACK to float
    x = x*(1.5f-xhalf*x*x); // Newton step, repeating increases accuracy
    x = x*(1.5f-xhalf*x*x); // Newton step, repeating increases accuracy
    return x;
}

int next_Step_2d(double* X, double *Y, double *VX, double *VY, double *M, double dt, double G, int SIZE, int SelectId){
    int i, j, new_id = SelectId;
    for(i = 0; i < SIZE; i++){
    	if(M[i]==0.0)break;
        double Ri = 1.0 / InvSqrt(M[i]);
        for(j = i + 1; j < SIZE; j++){
            double dx = X[j] - X[i];
            double dy = Y[j] - Y[i];
            double inv_L = InvSqrt(dx * dx + dy * dy);
            double Rj = 1.0 / InvSqrt(M[j]+0.1);
            // collide condition  L < (Ri + Rj) * k
            if(2.0 < inv_L *(Ri + Rj)){
            	//Merch Two Body
            	double m = M[i] + M[j];
                double x = (M[i] * X[i] + M[j] * X[j]) / m;
                double y = (M[i] * Y[i] + M[j] * Y[j]) / m;
                double vx = (M[i] * VX[i] + M[j] * VX[j]) / m;
                double vy = (M[i] * VY[i] + M[j] * VY[j]) / m;
                X[i] = x; X[j] = x;
                Y[i] = y; Y[j] = y;
                VX[i] = vx; VX[j] = vx;
                VY[i] = vy; VY[j] = vy;
                M[i] = m; M[j] = 0;
                if(SelectId == j)
                	new_id = i;
            }else{
            	double alpha = inv_L * inv_L * inv_L;
                double accx = G * dx * alpha;
                double accy = G * dy * alpha;
                VX[j] -= (M[i] * accx )* dt *0.5;
                VY[j] -= (M[i] * accy )* dt *0.5;
                VX[i] += (M[j] * accx )* dt *0.5;
                VY[i] += (M[j] * accy )* dt *0.5;
            }
        }
    }
    return new_id;
}

//double myrand(){
//	return (double)(rand() % 10000)/10000.0;
//}
//
//int main(){
//	int size = 1000;
//	double *X = (double*)calloc(size,sizeof(double));
//	double *Y = (double*)calloc(size,sizeof(double));
//	double *VX = (double*)calloc(size,sizeof(double));
//	double *VY = (double*)calloc(size,sizeof(double));
//	double *M = (double*)calloc(size,sizeof(double));
//	double dt = 0.5;
//	double G = 10.0;
//	int i;
//
//	for(i=0;i<size;i++){
//		X[i] = myrand()*1000.0;
//		Y[i] = myrand()*1000.0;
//		VX[i] = myrand()*1.0;
//		VY[i] = myrand()*1.0;
//		M[i] = myrand()*10.0;
//	}
//
//	for(i=0;i<10;i++){
//		clock_t start = clock();
//		next_Step_2d(X, Y, VX, VY, M, dt, G, 1000);
//		clock_t end = clock();
//		printf("%d\n",end - start);
//	}
//	for(i=0;i<size;i++){
//		printf("%f\n",M[i]);
//	}
//
//	for(i=0;i<size;i++){
//		free(X);
//		free(Y);
//		free(VX);
//		free(VY);
//		free(M);
//	}
//
//	return 0;
//}
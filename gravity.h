#ifndef _GRAVITY_H
#define _GRAVITY_H

// return 1.0f / sqrt(x)
float InvSqrt(float x);

// simulate one step of dt
int next_Step_2d(double* X, double *Y, double *VX, double *VY, double *M, double dt, double G, int SIZE, int SelectId);

#endif
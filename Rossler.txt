#include <windows.h>
#include <iostream>
#include <stdio.h>
#include <math.h>

using namespace std;            // Esto lo usa la función cin.ignore()

#define PI 3.141592
#define CENTRO 350  
#define MAXIMO 700             //Dibujamos en un cuadrado de 700 x 700
#define MARCADOR 5            //Longitud de la cruz del marcador para señalar el centro o el maximo de la pantalla

int main()                      // Atractor de Rossler dibujando los puntos como iteraciones desde (x0,y0)
{

    int puntox = 0;
    int puntoy = 0;            
    double xdosd=0;
    double ydosd=0;         
    int angulo = 60;            // Estos son los puntos que se dibujan en la pantalla siempre 2D. Angulo del isometrico    
    double xk = 0.0;
    double xkk = 0.0;
    double fxk = 0.0;
    double fxkk = 0.0;
    double yk = 0.0;
    double ykk = 0.0;
    double fyk = 0.0;
    double fykk = 0.0;         
    double zk = 0.0;        
    double zkk = 0.0;   
    double fzk = 0.0;
    double fzkk = 0.0;          // Estos son los puntos reales del atractor. Se usan k y k+1 valores para puntos y la funcion
    double a = 0.2;
    double b = 0.2;              
    double c = 5.7;            
    double dt = 0.04;             // Parametros del atractor de Rossler e incremento para la resolucion por metodo de Heun
    double escala = 30.0;        // Factor de escala 

    int totalpuntos = 10000;
    int puntosfuera = 0;
    int puntosempieza = 100;      // Total de puntos, puntos fuera del area de dibujo, puntos que se salta al principio
    int i = 0;                   // Un contador

    //Get a console handle and a handle to device context. Choose the color of the points
    HWND myconsole = GetConsoleWindow();
    HDC mydc = GetDC(myconsole);
    COLORREF COLOR = RGB(255, 255, 255);

    cout << "Atractor de Rossler H(x,y,z) = (-y-z, x+ay,b+x*z-c*z) \n";

    while (totalpuntos != 0)    // Este bucle es el principal
    {
        puntosfuera = 0;        //Inicializar para la siguiente vuelta
        cout << "Total de puntos: (10000) ";
        cin >> totalpuntos;
        cout << "Escala: (30)";
        cin >> escala;
        cout << "Angulo iso: (60 o 6)";
        cin >> angulo;
        cout << "c: (5.7)";
        cin >> c;

        // Dibujar los ejes positivos para z, y, x en este orden usando marcadores
        for (i = 0; i <= MARCADOR; i++) {
            xdosd = 0;
            ydosd = -i;
            puntox = (CENTRO / escala) * xdosd + CENTRO;
            puntoy = (CENTRO / escala) * ydosd + CENTRO;
            SetPixel(mydc, puntox, puntoy, COLOR);
        }
        for (i = 0; i <= MARCADOR; i++) {
            xdosd = i * cos ((180/PI)*(angulo-30));
            ydosd = i * cos((180/PI)*angulo);
            puntox = (CENTRO / escala) * xdosd + CENTRO;
            puntoy = (CENTRO / escala) * ydosd + CENTRO;
           
            SetPixel(mydc, puntox, puntoy, COLOR);
        }
        for (i = 0; i <= MARCADOR; i++) {
            xdosd = -i * cos((180 / PI) * (angulo - 30));
            ydosd = i * cos((180 / PI) * angulo);
            puntox = (CENTRO / escala) * xdosd + CENTRO;
            puntoy = (CENTRO / escala) * ydosd + CENTRO;
            SetPixel(mydc, puntox, puntoy, COLOR);
        } 


        //Dibuja el atractor de Rossler
        for (i = 0; i <= totalpuntos; i++)
        {
            //Todos los puntos inicializados a 0. Calculo el atractor usando la ecuacion de Henun
            // xk esta inicializado a 0,0,0
            // f(xk) 
            fxk = -1*(yk +zk);
            fyk = xk + a*yk;
            fzk = b + zk* (xk - c);
            // f(xk+1)
            fxkk = -1 * ((yk + dt * fyk) + (zk + dt * fzk));
            fykk = (xk + dt * fxk) + a * (yk + dt * fyk);
            fzkk = b + (zk + dt * fzk) * ((xk + dt * fxk) - c);
            // xk+1
            xkk = xk + (dt / 2) * (fxk + fxkk);
            ykk = yk + (dt / 2) * (fyk + fykk);
            zkk = zk + (dt / 2) * (fzk + fzkk);
            // Guardo los valores para la siguiente iteracion
            xk = xkk;
            yk = ykk;
            zk = zkk;
            //Paso los puntos 3D a 2D
            xdosd = 0 + ykk * cos((180 / PI) * (angulo - 30)) - xkk * cos((180 / PI) * (angulo - 30));
            ydosd = -zkk + ykk * cos((180 / PI) * angulo) + xkk * cos((180 / PI) * angulo);
            //Y por fin reescalo y centro los puntos en pantalla
            puntox = (CENTRO / escala) * xdosd + CENTRO;
            puntoy = (CENTRO / escala) * ydosd + CENTRO;    
            /* cout << "Punto xk" << xk << "  Punto yk" << yk << "  Punto zk" << zk << "\n"; */
            Sleep (2);
            SetPixel(mydc, puntox, puntoy, COLOR);
            if (puntox > MAXIMO || puntox <0 || puntoy > MAXIMO || puntoy < 0)
                puntosfuera++;
        }
        cout << "Puntos fuera de pantalla: " << puntosfuera << "\n";
        getchar();               //De momento esto para que no se borre la pantalla
        xk = yk = zk = 0;       // Hay que reinicializar para las siguientes vueltas
    }

    // Cierre del programa
    ReleaseDC(myconsole, mydc);
    cin.ignore();
    return 0;
}
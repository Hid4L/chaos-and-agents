#include <windows.h>
#include <iostream>
#include <stdio.h>
#include <math.h>

using namespace std;            // Esto lo usa la función cin.ignore()

#define CENTRO 350  
#define MAXIMO 700             //Dibujamos en un cuadrado de 700 x 700
#define MARCADOR 10            //Longitud de la cruz del marcador para señalar el centro o el maximo de la pantalla

int main()                      // Atractor de Henon dibujando los puntos como iteraciones desde (x0,y0)
{

    int puntox = 0;    
    int puntoy = 0;              // Estos son los puntos que se dibujan en la pantalla. x0 e y0 se inicializan a 0,0
    double x = 0.0;
    double xx = 0.0;
    double y=0.0;
    double yy = 0.0;               // Estos son los puntos reales del atractor. Se usan dos valores para realimentar la ecuacion
    double a = 1.4;
    double b = 0.3;               // Parametros del atractor de Henon
    double maximo = 1.5;          // Maximo valor del eje x. El eje x y el eje y van a escala 
   
    int totalpuntos = 100000;  
    int puntosfuera = 0;
    int puntosempieza = 100;      // Total de puntos, puntos fuera del area de dibujo, puntos que se salta al principio
    int i = 0;                   // Un contador

    //Get a console handle and a handle to device context. Choose the color of the points
    HWND myconsole = GetConsoleWindow();
    HDC mydc = GetDC(myconsole);
    COLORREF COLOR = RGB(255, 255, 255);

    cout << "Atractor de Henon H(x,y) = (y+1-ax2, bx) \n";
    

    while (totalpuntos != 0)    // Este bucle es el principal
    {
        puntosfuera = 0;        //Inicializar para la siguiente vuelta
        cin >> totalpuntos;

        // Dibujar los ejes usando marcadores
        for (puntox = CENTRO - MARCADOR; puntox <= CENTRO+MARCADOR; puntox++)
            SetPixel(mydc, puntox, CENTRO, COLOR);
        for (puntoy = CENTRO - MARCADOR; puntoy <= CENTRO+MARCADOR; puntoy++)
            SetPixel(mydc, CENTRO, puntoy, COLOR);

        //Dibuja el atractor de Henon
        for (i = 0; i <= totalpuntos; i ++)
        {
            xx = y + 1 - a * pow(x,2);
            yy = b * x;
            x = xx;
            y = yy;
            //Calculo el atractor
            puntox = (CENTRO / maximo) * xx + CENTRO;
            puntoy = (CENTRO / maximo) * yy+ CENTRO;     //Calculo puntos en pantalla
            /* cout << xx << "   " << puntox << "   " << yy << "   " << puntoy << "\n";
            getchar(); */
            SetPixel(mydc, puntox, puntoy, COLOR);
            if (puntox > MAXIMO || puntox <0 || puntoy > MAXIMO || puntoy < 0)
                puntosfuera++;
        }
        cout << "Puntos fuera de pantalla: " << puntosfuera << "\n";
        getchar();   //De momento esto para que no se borre la pantalla
    }

    // Cierre del programa
    ReleaseDC(myconsole, mydc);
    cin.ignore();
    return 0;
}





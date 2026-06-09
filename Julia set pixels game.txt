#include <windows.h>
#include <iostream>
#include <stdio.h>
#include <math.h>

using namespace std;            // Esto lo usa la función cin.ignore()

#define PANTALLA 320           //Dibujamos en un cuadrado de 700 x 700...
#define XYMAXIMO 2.0             //... que corresponde a la coordenada maxima y mínima en el plano z
                               // La division debe tener pocos decimales para que el dibujo no empiece a hacer cosas raras

int main()                      // Pixel game - dibuja conjuntos de Julia
{

    int puntox = 0;
    int puntoy = 0;              // Estos son los puntos que se dibujan en la pantalla. x0 e y0 se inicializan a 0,0
    int refinamientos = 0;       // Numero de refinamientos que se van a hacer
    int i = 0;                   
    int j = 0;                   // Un contador

    double x = 0.0;
    double y = 0.0;             
    double moduloxy;            // Estos son los puntos que barrerán el plano imaginario
    double xcopia = 0.0;
    double ycopia = 0.0;
    double xcopiaiterada = 0.0;
    double ycopiaiterada = 0.0;             // Estos son los puntos que se usan para las iteraciones
    double xc = 0.0;
    double yc = 0.0;            
    double moduloc = 0.0;       // El valor c de z -> z2 + c 
    double r = 0.0;             // El máximo de modulo de c y 2

    

    //Get a console handle and a handle to device context. Choose the color of the points
    HWND myconsole = GetConsoleWindow();
    HDC mydc = GetDC(myconsole);
    COLORREF BLANCO = RGB(255, 255, 255);
    COLORREF NEGRO = RGB(0, 0, 0);

    cout << "Valores real e imaginario de c para z -> z2 + c: \n";
    cin >> xc;
    cin >> yc;
    cout << "Refinamientos: \n";
    cin >> refinamientos;
    
    for (i = refinamientos; i >= 0; i--)    // Empezamos por el refinamiento interior para poder ver los colores
    {
        //Dibuja los distintos refinamientos. i va a ser el número de iteraciones. Se dibuja por líneas horizontales
        for ( y= -1*XYMAXIMO; y <= XYMAXIMO; y= y + (XYMAXIMO/PANTALLA))             // Fija el valor vertical
        {
            for (x = -1*XYMAXIMO; x <= XYMAXIMO; x = x + (XYMAXIMO/PANTALLA))     // Bucle para dibujar una línea horizontal
            { 
                    xcopia = x;
                    ycopia = y;     // x e y se copian para poder hacer las iteraciones sin perder los puntos originales 
                    for (j = 0; j <= i ; j++)                                   // Hace la iteración correspondiente
                    {                                        
                        xcopiaiterada = pow(xcopia, 2) - pow(ycopia, 2) + xc;
                        ycopiaiterada = 2 * xcopia * ycopia + yc;
                        xcopia = xcopiaiterada;
                        ycopia = ycopiaiterada;                                     // Con estas dos variables se hace la iteración
                    }
                    // Y ahora se ve si ese punto escapó, y si es así se dibuja. Hago los cálculos paso a paso
                    moduloxy = pow(xcopia, 2) + pow(ycopia, 2);                      // En realidad es el cuadrado del módulo
                    moduloc = sqrt(pow(xc, 2) + pow(yc, 2));                         // Este sí es el módulo
                    r = max(moduloc, 2)*max(moduloc,2);
                    if (moduloxy > r) {           
                         puntox = (PANTALLA / XYMAXIMO) * x + PANTALLA;               //Calculo puntos en pantalla y los dibujo
                         puntoy = -(PANTALLA / XYMAXIMO) * y + PANTALLA;     
                         if (i % 2 == 0) SetPixel(mydc, puntox, puntoy, BLANCO);
                         else SetPixel(mydc, puntox, puntoy, NEGRO);
                    }
            }
        }
    }

    // Cierre del programa
    for (j = 0; j <= 30 ;j++)  //Cursor para abajo para que no chafe el gráfico
        cout << "\n";
    cout << "Listo";       
    ReleaseDC(myconsole, mydc);
    cin.ignore();
    return 0;
}
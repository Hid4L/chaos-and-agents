#include <iostream>
#include <windows.h>        //Para los graficos
#include <chrono>           //Para los tiempos
#include <thread>

using namespace std;

#define PI 3.141592 
#define GUSANOS 5                    //Numero de gusanos en la simulacion
#define LONGITUD 7                   //Como de largo es el rastro del gusano -2 posiciones: la cola y la que sera la nueva cabeza. Longitud 7 -> cuerpo del gusano es 5 pixels
#define MEMORIA 8                    //De cuantas cosas se acuerda el gusano 
#define VISTA 1                      //El gusano ve un cuadrado de VISTA x VISTA desde la cabeza 
#define VIDA 1800                    //Los ciclos de simulacion que vive un gusano, dependiendo de si ha comido,... segun el comportamiento
#define PESO 5                       //Los gusanos que se necesitan para mover alog, o para reunirse
#define CICLOSIMULACION 1000         //Cuantos ciclos vagan en total, por si hay que parar la simulacion en algun momento
#define DISTANCIAMERODEANDO 10       //La distancia que usan en Merodear()
#define DISTANCIAEXPLORACION 1000    //La distancia a la que se alejan los gusanos de un punto antes de hacer algo mas

#define lineashorizontales 5
#define lineasverticales 5

/* Definicion de los gusanos */
int puntox[GUSANOS][LONGITUD];
int puntoy[GUSANOS][LONGITUD];              //Las coordenadas x,y de cada gusano.Incluye cola - cuerpo - cabeza 
int incrementox[9] = { 0,  0,  1, 1, 1, 0, -1, -1, -1 };            //Esta definicion esta repetida en mas sitios
int incrementoy[9] = { 0, -1, -1, 0, 1, 1,  1,  0, -1 };
//                         N  NE  E  SE S   SO  O  NO
//                         1  2   3  4  5   6   7  8
//Traduce puntos cardinales N es 1, NE 2,... a incrementos. Los puntos cardinales coinciden con los normales. 
//Punto x,y  0,0 esta en la esquina superior ixquierda de la pantalla. Eje x de izquierda a derecha. Eje y de arriba a a abajo   
//Dependiendo la direccion, se hace un +/-1 incremento en direccion x o y 
int vision[3][3];                            //El cuadrado de vision del gusano. 9 veces, una para el centro y 8 para las 8 posibles direcciones: 1, 2, ...
int escaneo[16];                             //Escaneo alrededor del gusano
int estado[GUSANOS];                         //Que esta haciendo el gusano
//Estado 0 vagando.  ...  Estado 9 muerto
int ciclos[GUSANOS];                        //Contador de simulaciones que se han llevado a cabo para cada gusano, como de viejo es cada gusano
int color[GUSANOS];                         //El color de cada gusano, que puede usarse para evidenciar el estado: esta durmiendo (azul), esta vagando (blanco),...
int memoria[GUSANOS][MEMORIA];              //Cosas que sabe el gusano
//Posiciones 0,1 casa. 2,3 donde nacieron. 4,5 miga. 6,7 objetivo temporal

/* Definicion de la mente global */
int menteglobal = 0;                        //El estado de la mente global, basado en el estado de los gusanos o en decisiones propias
int simulaciones = 0;                       //Numero de simulaciones totales
int mapa_x[2100];
int mapa_y[2100];
static int coordenada = 0;

/* Comportamientos */
int Vagar(int);
int Acercarse(int, int, int);
double anguloAleatorio;

/* Funciones de soporte */
void InicializaGusanos();              //Pone a los gusanos en su lugar de inicio, y tambien en us estado de inicio -color y estado-
void CalculaGusano(int, int);          //Traduce direccion a movimiento, y genera el cuerpo del gusano    
void DibujaGusanos();                  //Dibuja todos los gusanos. En el futuro a lo mejor no dibujo, solo simulo, o dibujo cada X simulaciones si la velocidad de computo es baja
int Escanea(int);                        //Genera vector de escaneado
void Mira(int);                           //Genera matriz de vision
void InterpretaCampoVision(int);
int InterpretaCampoEscaneado(int);     //Decuelve la direccion de movimiento


/* Manejo de graficos */
//Get a console handle and a handle to device context. Choose the color of the points
HWND myconsole = GetConsoleWindow();
HDC mydc = GetDC(myconsole);
COLORREF BLANCO = RGB(255, 255, 255);
COLORREF NEGRO = RGB(0, 0, 0);
COLORREF AZUL = RGB(0, 0, 255);
COLORREF AMARILLO = RGB(255, 255, 0);
COLORREF ROJO = RGB(255, 0, 0);

int main()
{

    /* Escenario de la simulacion */
    int linea_horizontal[lineashorizontales] = { 100,200,300,125,175 };
    int linea_horizontal_inicio[lineashorizontales] = { 100,200,100,225,225 };
    int linea_horizontal_final[lineashorizontales] = { 300,300,200,275,275 };
    int linea_vertical[lineasverticales] = { 100,200,300,225,275 };
    int linea_vertical_inicio[lineasverticales] = { 100,200,100,125,125 };
    int linea_vertical_final[lineasverticales] = { 300,300,200,175,175 };
    int muro_x;
    int muro_y;

    /* Variables para los gusanos */
    int gusano;
    int escaneado;

    /* Contadores,... */
    int i;
    int j;

    /* Dibuja el escenario */
    for (i = 0; i <= lineashorizontales; i++)
    {
        for (j = linea_horizontal_inicio[i]; j <= linea_horizontal_final[i]; j++)
        {
            muro_x = j;
            muro_y = linea_horizontal[i];
            SetPixel(mydc, muro_x, muro_y, AZUL);
        }
    }
    for (i = 0; i <= lineasverticales; i++)
    {
        for (j = linea_vertical_inicio[i]; j <= linea_vertical_final[i]; j++)
        {
            muro_x = linea_vertical[i];
            muro_y = j;
            SetPixel(mydc, muro_x, muro_y, AZUL);
        }
    }

    for (i = 0; i < 20; i++)
        cout << endl;

    InicializaGusanos();
    srand(time(NULL));


    /* 17 - octubre. Estrategia de escanear, mober y fijar. Los gusanos son mas como maquinas
    *  A ver que pasa
    *  18 - Paredes detectadas, esquinas detectadas
    *  19 - Picones detectados
    *  19 - ahora que deje de seguir el perimetro cuando solo encuentre blancos, ya esta
    *  19 - y que rebote contra la pared si se la encuentra de frente, ya esta... para 1 gusano
    */

    while (menteglobal == 0)
    {

        DibujaGusanos();

        for (gusano = 0; gusano < GUSANOS; gusano++)
        {

            //Primero escanea
            //En el momento que esta detectando algo azul, pasa a estado 2
            escaneado = Escanea(gusano);

            if (escaneado == 1 && estado[gusano] == 1)         //Detecta algun azul, y estaba explorando. Entonces pasa al estado 2
            {
                estado[gusano] = 2;
                //cout << "Algo ..";
            }

            if (escaneado == 2 && estado[gusano] == 2)        //Ningun azul, y venia de seguir una pared. Entonces pasa al estado 0
            {
                estado[gusano] = 0;
                //cout << "Abandonando pared...";
            }

            // - > ESTOIY AQUI
            if ( (escaneado == 3 || escaneado == 4 || escaneado == 5 || escaneado == 6) )
                //&& estado[gusano] == 1)                     //Estaba por ahi explorando, y se da de frente contra una pared blanca
            {
                estado[gusano] = 0;
                //cout << "De cabeza contra la pared";
            }

            //Mira antes de mover, a ver si tiene via libre. Asi sabra si es un picon, por ejemplo
            Mira(gusano);
            InterpretaCampoVision(gusano);

            //Pone a los gusanos a andar
            if (estado[gusano] == 0)
            {
                //Ninguna direccion preferida
                anguloAleatorio = (rand() % 360 + 1) * (PI / 180);
                //anguloAleatorio = 270 * (PI / 180);
                //cout << anguloAleatorio; 
                if (escaneado == 3)                                        //Saliendo de pared al Norte, elegir angulos entre 10 y 170 para alejarse
                    anguloAleatorio = ((rand() % (170 - 10 + 1) + 10)) * (PI / 180);
                    //anguloAleatorio = 90 * (PI / 180);

                if (escaneado == 4)                                        //Pared al Este, elegir angulos entre 100 y 260
                    anguloAleatorio = ((rand() % (260 - 100 + 1) + 100)) * (PI / 180);
                    //anguloAleatorio = 180 * (PI / 180);

                if (escaneado == 5)                                        //Pared al Sur, elegir angulos entre 190 y 350
                    anguloAleatorio = ((rand() % (350 - 190 + 1) + 190)) * (PI / 180);
                    //anguloAleatorio = 270 * (PI / 180);

                if (escaneado == 6)                                        //Pared al Oeste, elegir angulos entre 270 y 350. Paso del cuadrante 0 a 90
                    //anguloAleatorio = ((rand() % (350 - 270 + 1) + 270)) * (PI / 180);
                    anguloAleatorio = 280 * (PI / 180);


                //cout << anguloAleatorio;
                memoria[gusano][6] = puntox[gusano][LONGITUD - 1] + DISTANCIAEXPLORACION * cos(anguloAleatorio);
                memoria[gusano][7] = puntoy[gusano][LONGITUD - 1] + DISTANCIAEXPLORACION * sin(anguloAleatorio);
                //memoria[gusano][6] = 400;     Para fijar direcciones
                //memoria[gusano][7] = 150;
                estado[gusano] = 1;
            }

            //Estado 1, va andando hacia un punto objetivo
            if (estado[gusano] == 1) {
                CalculaGusano(gusano, Acercarse(gusano, memoria[gusano][6], memoria[gusano][7]));
            }

            // Si el estado es 2, la funcion InterpretaCampoEscaneado() es la que manda el movimiento
            if (estado[gusano] == 2) {
                CalculaGusano(gusano, InterpretaCampoEscaneado(gusano));
            }

        }

        if (coordenada >= 900)   //El % del perimetro, el perimetro son 1000 puntos
            menteglobal = 1;

    }


    /*  Cierre del programa  */

    cout << "Simulacion completada." << endl;
    //Dibuja el mapa a la derecha
    for (i = 0; i <= coordenada; i++)
        SetPixel(mydc, mapa_x[i] + 400, mapa_y[i], BLANCO);

    //Suelta la consola grafica
    ReleaseDC(myconsole, mydc);
    cin.ignore();
    return (0);

}




//Inicializa a los gusanos al inicio de la simulacion. Todos en un sitio, al azar,... 
//Les pone en una posicion, un color y un estado
void InicializaGusanos()
{
    int i;
    int j;      //Contadores

    //Estado 0 vagando. Ciclos 0 esto es, su edad. Color blanco
    //Les mete en la memoria donde esta casa
    for (i = 0; i < GUSANOS; i++)
    {
        estado[i] = 0;              //El estado 0 lo guardo para Vagar()
        ciclos[i] = 0;
        color[i] = AMARILLO;        //Para que no se vean entre ellos. Los gusano deben ser ciegos al amarillo
        memoria[i][0] = 150;        //Casa
        memoria[i][1] = 150;
    }

    //Posiciona a todos los gusanos en la gusanera
    for (i = 0; i < GUSANOS; i++)
    {
        for (j = 0; j < LONGITUD; j++)              //Crea el cuerpo del gusano, los 5 pixeles en el mismo punto
        {
            puntox[i][j] = memoria[i][0];
            puntoy[i][j] = memoria[i][1];
        }
    }

}

//Dibuja todos los gusanos en cada ciclo. Si GUSANOS es 3, el nombre de los gusanos es 0,1 y 2
void DibujaGusanos()
{
    int gusano;
    int j;          //Contador

    using namespace std::this_thread;     // sleep_for, sleep_until
    using namespace std::chrono_literals; // ns, us, ms, s, h, etc.
    using std::chrono::system_clock;

    for (gusano = 0; gusano < GUSANOS; gusano++)
    {
        SetPixel(mydc, puntox[gusano][0], puntoy[gusano][0], NEGRO);       //El punto 0 que es la cola lo borra siempre. 
        for (j = 1; j < (LONGITUD - 1); j++)                               //Ojo, desde 1 y hasta dos posiciones menos que LONGITUD. Si LONGITUD = 7, longitud del gusano 5
            //SetPixel(mydc, puntox[gusano][j], puntoy[gusano][j], color[gusano]);
            SetPixel(mydc, puntox[gusano][j], puntoy[gusano][j], AMARILLO);
    }
    //sleep_for(200us);       // Para que no se mueva demasiado rapido. Igual con varios gusanos no hace ni falta
}

//Calcula el cuerpo gusano en una direccion, y  estos son los 2 argumentos que recibe
//13 octubre - impedir que se choquen contra puntos BLANCOS. Si va a chocar contra un punto blanco, ese ciclo no se mueve
void CalculaGusano(int gusano, int direccion)
{
    int j = 0;                  //Contador

    //La cabeza la calcula siempre
    puntox[gusano][LONGITUD - 1] = puntox[gusano][LONGITUD - 2] + incrementox[direccion];
    puntoy[gusano][LONGITUD - 1] = puntoy[gusano][LONGITUD - 2] + incrementoy[direccion];

    //El cuerpo se desplaza solo si la cabeza no se la va a pegar contra un pixel blanco. Si no, no se mueve esta vez, espera a la siguiente direccion
    if (GetPixel(mydc, puntox[gusano][LONGITUD - 1], puntoy[gusano][LONGITUD - 1]) != BLANCO)
        for (j = 0; j < (LONGITUD - 1); j++)                            //Mueve las posiciones dentro de la matriz para crear la sensacion de movimiento
        {
            puntox[gusano][j] = puntox[gusano][j + 1];
            puntoy[gusano][j] = puntoy[gusano][j + 1];
        }
}


//Genera el campo de vision vision[][] 
void Mira(int gusano)
{

    //using namespace std::this_thread;     // sleep_for, sleep_until
    //using namespace std::chrono_literals; // ns, us, ms, s, h, etc.
    //using std::chrono::system_clock;

    int i = 0;
    int j = 0;                                      //Contadores
    int puntotempx;
    int puntotempy;                                 //Puntos que van barriendo el campo de vision

    int negro = 0;                                  //Codificacion de color a numero. Las mayusculas son para los colores en RGB
    int blanco = 1;
    int azul = 2;
    int amarillo = 3;
    COLORREF colordelpixel;

    //Inicializo el vector, al ser variable global puede dar problemas
    for (i = -VISTA; i <= VISTA; i++)
        for (j = -VISTA; j <= VISTA; j++)
            vision[i + 1][j + 1] = negro;

    //for (i = -VISTA; i <= VISTA; i++)
        //for (j = -VISTA; j <= VISTA; j++)
            //cout << vision[i + 1][j + 1];

    for (i = -VISTA; i <= VISTA; i++)
    {
        puntotempx = puntox[gusano][LONGITUD - 1] + i;
        for (j = -VISTA; j <= VISTA; j++)
        {
            puntotempy = puntoy[gusano][LONGITUD - 1] + j;
            //Visualiza el campo
            //SetPixel(mydc, puntotempx, puntotempy, ROJO);
            //sleep_for(100000us);
            //SetPixel(mydc, puntotempx, puntotempy, NEGRO);
            //
            colordelpixel = GetPixel(mydc, puntotempx, puntotempy);
            if (colordelpixel == NEGRO)
                vision[i + 1][j + 1] = negro;
            if (colordelpixel == AMARILLO)
                vision[i + 1][j + 1] = amarillo;
            if (colordelpixel == BLANCO)
                vision[i + 1][j + 1] = blanco;
            if (colordelpixel == AZUL)
                vision[i + 1][j + 1] = azul;
        }
    }
}

//Lo que hace con el campo de vision
//De momento los puntos azules los pasa a blancos y los guarda en un vector de memoria
void InterpretaCampoVision(int gusano)
{
    int i = 0;
    int j = 0;                                      //Contadores
    int puntotempx;
    int puntotempy;                                 //Puntos que van barriendo el campo de vision

    int negro = 0;                                  //Codificacion de color a numero. Las mayusculas son para los colores en RGB
    int blanco = 1;
    int azul = 2;
    int amarillo = 3;

    for (i = -VISTA; i <= VISTA; i++)
    {
        puntotempx = puntox[gusano][LONGITUD - 1] + i;
        for (j = -VISTA; j <= VISTA; j++)
        {
            puntotempy = puntoy[gusano][LONGITUD - 1] + j;
            if (vision[i + 1][j + 1] == azul)
            {
                mapa_x[coordenada] = puntotempx;
                mapa_y[coordenada] = puntotempy;
                coordenada++;
                SetPixel(mydc, puntotempx, puntotempy, BLANCO);
            }
        }
    }
}


//Crea el vector de escaneo escaneo[]
int Escanea(int gusano)
{

    //using namespace std::this_thread;     // sleep_for, sleep_until
    //using namespace std::chrono_literals; // ns, us, ms, s, h, etc.
    //using std::chrono::system_clock;

    int i = 0;
    int j = 0;
    int k = 0;                                          //Contadores
    int pixeles = 0;

    int negro = 0;                                  //Codificacion de color a numero. Las mayusculas son para los colores en RGB
    int blanco = 1;
    int azul = 2;
    int amarillo = 3;
    COLORREF colordelpixel;

    //Inicializo el vector, al ser variable global parece que daba problemas
    for (i = 0; i <= 15; i++)
        escaneo[i] = negro;

    //Empieza en posicion 0, la primera posicion para ver el Norte. Costruyo el vector por filas, y con mucho cuidado

    for (i = 0; i <= 3; i++)                           //Fila de arriba, empezando por posicion 0
    {
        colordelpixel = GetPixel(mydc, puntox[gusano][LONGITUD - 1] + i - 1, puntoy[gusano][LONGITUD - 1] - 2);

        //Visualiza el campo
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] + i - 1, puntoy[gusano][LONGITUD - 1] - 2, ROJO);
        //sleep_for(100000us);
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] + i - 1, puntoy[gusano][LONGITUD - 1] - 2, NEGRO);
        //

        if (colordelpixel == NEGRO)
            escaneo[i] = negro;
        if (colordelpixel == AMARILLO)
            escaneo[i] = amarillo;
        if (colordelpixel == BLANCO)
            escaneo[i] = blanco;
        if (colordelpixel == AZUL)
            escaneo[i] = azul;
    }

    for (i = 4; i <= 7; i++)
    {
        colordelpixel = GetPixel(mydc, puntox[gusano][LONGITUD - 1] + 2, puntoy[gusano][LONGITUD - 1] + i - 5);

        //Visualiza el campo
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] + 2, puntoy[gusano][LONGITUD - 1] + i - 5, ROJO);
        //sleep_for(100000us);
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] + 2, puntoy[gusano][LONGITUD - 1] + i - 5, NEGRO);
        //

        if (colordelpixel == NEGRO)
            escaneo[i] = negro;
        if (colordelpixel == AMARILLO)
            escaneo[i] = amarillo;
        if (colordelpixel == BLANCO)
            escaneo[i] = blanco;
        if (colordelpixel == AZUL)
            escaneo[i] = azul;
    }


    for (i = 8; i <= 11; i++)
    {
        colordelpixel = GetPixel(mydc, puntox[gusano][LONGITUD - 1] + 9 - i, puntoy[gusano][LONGITUD - 1] + 2);

        //Visualiza el campo
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] + 9 - i, puntoy[gusano][LONGITUD - 1] + 2, ROJO);
        //sleep_for(100000us);
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] + 9 - i, puntoy[gusano][LONGITUD - 1] + 2, NEGRO);
        //

        if (colordelpixel == NEGRO)
            escaneo[i] = negro;
        if (colordelpixel == AMARILLO)
            escaneo[i] = amarillo;
        if (colordelpixel == BLANCO)
            escaneo[i] = blanco;
        if (colordelpixel == AZUL)
            escaneo[i] = azul;
    }


    for (i = 12; i <= 15; i++)
    {
        colordelpixel = GetPixel(mydc, puntox[gusano][LONGITUD - 1] - 2, puntoy[gusano][LONGITUD - 1] + 13 - i);

        //Visualiza el campo
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] - 2, puntoy[gusano][LONGITUD - 1] + 13 - i, ROJO);
        //sleep_for(100000us);
        //SetPixel(mydc, puntox[gusano][LONGITUD - 1] - 2, puntoy[gusano][LONGITUD - 1] + 13 - i, NEGRO);
        //

        if (colordelpixel == NEGRO)
            escaneo[i] = negro;
        if (colordelpixel == AMARILLO)
            escaneo[i] = amarillo;
        if (colordelpixel == BLANCO)
            escaneo[i] = blanco;
        if (colordelpixel == AZUL)
            escaneo[i] = azul;
    }

    //Verificar si hay algo detectado
    //for (i = 0; i <= 15; i++)
        //cout << escaneo[i] << ".";
    //cout << endl;

    // ESTOY AQUI  - >  Lo mismo para evitar que se quede pegado a una pared ya explorada. N, E, S y O. Esto ha pasado con 2 gusanos, claro
    //Empieza a seguir la pared, se encuentra un blanco, y se queda pegado - solucionar esto
    if (escaneo[14] == blanco && escaneo[4] == blanco && escaneo[15] == negro && escaneo[0] == negro && escaneo[1] == negro && escaneo[2] == negro && escaneo[3] == negro) {
        pixeles = 3;
        //cout << "N";
        return(pixeles);
    }
    if (escaneo[2] == blanco && escaneo[8] == blanco && escaneo[3] == negro && escaneo[4] == negro && escaneo[5] == negro && escaneo[6] == negro && escaneo[7] == negro) {
        pixeles = 4;
        //cout << "E";
        return(pixeles);
    }
    if (escaneo[6] == blanco && escaneo[12] == blanco && escaneo[7] == negro && escaneo[8] == negro && escaneo[9] == negro && escaneo[10] == negro && escaneo[11] == negro) {
        pixeles = 5;
        //cout << "S";
        return(pixeles);
    }
    if (escaneo[0] == blanco && escaneo[10] == blanco && escaneo[11] == negro && escaneo[12] == negro && escaneo[13] == negro && escaneo[14] == negro && escaneo[15] == negro) {
        pixeles = 6;
        //cout << "O";
        return(pixeles);
    }

    //Se da de frente contra una pared explorada al norte, este, sur y oeste. Se aleja y punto
    if (escaneo[15] == blanco && escaneo[0] == blanco && escaneo[1] == blanco && escaneo[2] == blanco && escaneo[3] == blanco)  {
        pixeles = 3;
        return(pixeles);
    }
    if (escaneo[3] == blanco && escaneo[4] == blanco && escaneo[5] == blanco && escaneo[6] == blanco && escaneo[7] == blanco)   {
        pixeles = 4;
        return(pixeles);
    }
    if (escaneo[7] == blanco && escaneo[8] == blanco && escaneo[9] == blanco && escaneo[10] == blanco && escaneo[11] == blanco) {
        pixeles = 5;
        return(pixeles);
    }
    if (escaneo[11] == blanco && escaneo[12] == blanco && escaneo[13] == blanco && escaneo[14] == blanco && escaneo[15] == blanco)  {
        pixeles = 6;
        return(pixeles);
    }

    //Ojo, que si todo esta negro alrededor tiene que seguir explorando
    //Si detecta algun blanco - o sea que no hay nada que explorar- devuelve 2
    for (i = 0; i <= 15; i++)
        if (escaneo[i] == blanco)
            pixeles = 2;

    //.. y ningun azul, devuelve 1, y este valor pisa al anterior
    for (i = 0; i <= 15; i++)
        if (escaneo[i] == azul) {
            pixeles = 1;
            return(pixeles);
        }

    return(pixeles);
}


//Devuelve una direccion. Basandose en calculos con el vector de escaneo
int InterpretaCampoEscaneado(int gusano)
{
    int i = 0;
    int j = 0;
    int negro = 0;                                  //Codificacion de color a numero. Las mayusculas son para los colores en RGB
    int blanco = 1;
    int azul = 2;
    int amarillo = 3;

    //int sumadelvector = 0;
    int sensor_norteazul;
    int sensor_surazul;
    int sensor_esteazul;
    int sensor_oesteazul;                            //Suma de los 3 sensores en cada una de las direcciones - azul
    int sensor_norteblanco;
    int sensor_surblanco;
    int sensor_esteblanco;
    int sensor_oesteblanco;                          //Suma de los 3 sensores en cada una de las direcciones - blanco
    int vectordeazules[16];
    int vectordeblancos[16];
    int direccion = 0;

    //Reinicia vectores
    for (i = 0; i <= 15; i++)
        vectordeazules[i] = 0;
    for (i = 0; i <= 15; i++)
        vectordeblancos[i] = 0;

    //Traduce azules a 1s
    for (i = 0; i <= 15; i++)
        if (escaneo[i] == azul)
            vectordeazules[i] = 1;

    //Traduce blancos a 1s
    for (i = 0; i <= 15; i++)
        if (escaneo[i] == blanco)
            vectordeblancos[i] = 1;

    sensor_norteazul = vectordeazules[0] + vectordeazules[1] + vectordeazules[2];
    sensor_esteazul = vectordeazules[4] + vectordeazules[5] + vectordeazules[6];
    sensor_surazul = vectordeazules[8] + vectordeazules[9] + vectordeazules[10];
    sensor_oesteazul = vectordeazules[12] + vectordeazules[13] + vectordeazules[14];

    sensor_norteblanco = vectordeblancos[0] + vectordeblancos[1] + vectordeblancos[2];
    sensor_esteblanco = vectordeblancos[4] + vectordeblancos[5] + vectordeblancos[6];
    sensor_surblanco = vectordeblancos[8] + vectordeblancos[9] + vectordeblancos[10];
    sensor_oesteblanco = vectordeblancos[12] + vectordeblancos[13] + vectordeblancos[14];


    //Detecta pared y via libre en la direccion de movimiento. LA utlima eleccion tiene prioridad, meter alguna condicion luego -gusanos pares, impares,...-
    //Detecta esquina es como detecta pared
    //Estas detecciones tienen prioridad, por eso se incluyen los return()
    if (sensor_norteazul >= 1 && vision[1][0] == negro)
    {
        direccion = 1;
        return (direccion);
    }
    if (sensor_esteazul >= 1 && vision[2][1] == negro)
    {
        direccion = 3;
        return (direccion);
    }
    if (sensor_surazul >= 1 && vision[1][2] == negro)
    {
        direccion = 5;

        return (direccion);
    }
    if (sensor_oesteazul >= 1 && vision[0][1] == negro) {
        direccion = 7;
        return (direccion);
    }

    //Picones. Detecta un punto azul al que quiere llegar, pero tiene que seguir la pared 2 incrementos mas antes de girar porque un trozo de nuro no le deja llegar
    if (sensor_norteazul >= 1 && vision[1][0] == blanco)
    {
        if (sensor_oesteblanco >= 1)
            direccion = 3;
        if (sensor_esteblanco >= 1)
            direccion = 7;
    }
    if (sensor_esteazul >= 1 && vision[2][1] == blanco)      //Punto azul por explorar esta al este, pero no puede llegar
    {
        if (sensor_norteblanco >= 1)                         //Norte estaba explorado, va al sur
            direccion = 5;
        if (sensor_surblanco >= 1)                           //Sur estaba explorado, va al norte
            direccion = 1;
    }
    if (sensor_surazul >= 1 && vision[1][2] == blanco)
    {
        //cout << sensor_oesteblanco << ".." << sensor_esteblanco << endl;
        if (sensor_oesteblanco >= 1)
            direccion = 3;
        if (sensor_esteblanco >= 1)
            direccion = 7;
    }
    if (sensor_oesteazul >= 1 && vision[0][1] == blanco)
    {
        if (sensor_norteblanco >= 1)
            direccion = 5;
        if (sensor_surblanco >= 1)
            direccion = 1;
    }

    //Comodin. Al menos que no se quede quieto. Podria mejorar detectando esquinas y picones, pero no creo que se gane mucho en terminos de deteccion

    if (direccion == 0)
        direccion = rand() % 8 + 1;

    return (direccion);

}

/* Acciones de los gusanos  */

//Anda de forma aleatoria. Direccion es hacia donde se va a mover del 1 al 8 (Luego se traducira en N a SO)
int Vagar(int gusano)
{
    int direccion;

    direccion = rand() % 8 + 1;
    return (direccion);
}



//Va a elegir una direccion al azar. Si la distancia al objetivo yendo en esa direccion es menor que la distancia a la que se encuentra, la usa
//Se obtiene un movimiento mas natural, como si el gusano olfateara el punto objetivo
int Acercarse(int gusano, int puntoenx, int puntoeny)
{
    int direccionPosible = 0;
    int direccion = 0;           //Esta direccion se inicializa a 0 para que entre en el while. direccionPosible es la direccion que considera
    int puntoxtemp = 0;
    int puntoytemp = 0;          //El punto hacia el que va. Lo uso para que se vea mejor el calculo, no usar formulas demasiado largas
    double distanciaCabeza = 0;
    double distancia = 0;        //Distancia de la cabeza al objetivo, y desde el punto al que se moveria al objetivo
    int i = 0;                   //Un contador

    distanciaCabeza = sqrt(pow((puntox[gusano][LONGITUD - 1] - puntoenx), 2) + pow((puntoy[gusano][LONGITUD - 1] - puntoeny), 2));
    while (direccion == 0)
    {
        direccionPosible = rand() % 8 + 1;                                                              //Elige una direccion al azar

        puntoxtemp = puntox[gusano][LONGITUD - 1] + incrementox[direccionPosible];
        puntoytemp = puntoy[gusano][LONGITUD - 1] + incrementoy[direccionPosible];                      //Este es el punto hacia el que podria moverse
        distancia = sqrt(pow((puntoxtemp - puntoenx), 2) + pow((puntoytemp - puntoeny), 2));

        if (distancia < distanciaCabeza)
            direccion = direccionPosible;                                                              //Si reduce distancia usando esa direccion, la elige y sale del while

        i++;                    //Para evitar que se quede en bucle, sale por algun sitio
        if (i > 16)
            direccion = direccionPosible;
    }
    return(direccion);
}
"""
Plantilla PONG per al Lab2 (Introducció a la Programació)
---------------------------------------------------------
Objectius didàctics (focalitzats en funcions):
- Practicar la definició i l'ús de funcions amb paràmetres i valors de retorn.
- Evitar variables globals.
- Enllaçar funcions que transformin l'estat del joc (posicions i velocitats).
- NO utilitzar classes, llistes ni diccionaris.
- Omple el codi on calgui. Mantén EXACTES els noms i signatures de les funcions.

Lliurament:
- Un únic fitxer Python: PNNN_TNN_P2_U1_U2.py
- Ha d'executar-se localment amb: `python PNNN_TNN_P2_U1_U2.py`
- Requereix pygame (instal·la amb `pip install pygame`).

Restriccions / Regles d'estil:
- Sense `class`, sense `list`, sense `dict` (les tuples estan permeses per a múltiples retorns).
- Aquest laboratori evita intencionadament sintaxi avançada (mètodes, assert, tuples explícites)
- Defineix i utilitza les funcions marcades com a TODO. No les reanomenis.
- Les constants es poden llegir però NO modificar-se durant l'execució.
- El bucle principal i la secció de renderització es proporcionen; no els canviïs ni els moguis.

Control anti copiar/enganxar amb IA:
- Has de poder explicar al professor què fa cada funció
- Has de poder explicar seccions específiques del teu programa per verificar-ne la comprensió
"""

import sys      # Utilitzat només per a sys.exit(0): garanteix una terminació neta del programa a tots els SO
import pygame  # essencial per a tot el renderitzat i el joc
import random   # útil per aleatoritzar lleugerament coses (p. ex., direcció inicial de la pilota)

# ==============
# Constants del joc
# ==============

# Modifica-les aquí si vols canviar la mida del taulell
WIDTH = 900     # píxels
HEIGHT = 600    # ídem
FPS = 60        # Fotogrames per segon - No cal canviar-ho - per canviar les velocitats de pales/pilota canvia el següent ->

# Velocitats (píxels per fotograma aprox.) (els 3 valors es poden canviar a get_config() )
SPEED_PADDLE = 7
SPEED_BALL_X = 6
SPEED_BALL_Y = 5

# Colors RGB de fons i primer pla per defecte (es poden canviar a change_colors() )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Geometria: valors per defecte de pala i pilota (alguns es poden canviar a get_config() )
PADDLE_W = 14       # píxels
PADDLE_H = 110      # píxels - es pot canviar a get_config()
PADDLE_MARGIN = 30  # píxels - distància del marge
BALL_RADIUS = 9     # píxels - es pot canviar a get_config()
POINTS_END = 11     # puntuació per acabar una partida
SERVE_PAUSE = 300   # ms entre cada servei

# Tecles del jugador: Canvia-les aquí si prefereixes altres tecles
KEY_UP_LEFT = pygame.K_a            # a
KEY_DOWN_LEFT = pygame.K_z          # z
KEY_UP_RIGHT = pygame.K_UP          # fletxa AMUNT
KEY_DOWN_RIGHT = pygame.K_DOWN      # fletxa AVALL

# Indicador per jugar contra la màquina
play_against_machine = True    # False per defecte
# Crea una funció perquè l'usuari la pugui canviar opcionalment, si implementes el mode de "màquina intel·ligent"

# ==============================================================================
# Funcions a completar pels estudiants : configuració/posada a punt abans de començar
# ==============================================================================

def get_config() -> tuple[int, int, int, int, int]:
    """ Demana a l'usuari si vol modificar els principals paràmetres del joc:
    (alçada de la pala, velocitat de la pala, velocitat X de la pilota, velocitat Y de la pilota i radi de la pilota).
   
    Si l'usuari **no** vol obrir el menú de configuració, la funció
    simplement retorna els valors per defecte definits a l'inici del programa:
        (PADDLE_H, SPEED_PADDLE, SPEED_BALL_X, SPEED_BALL_Y, BALL_RADIUS)

    Si l'usuari respon **sí**, la funció hauria de:
      - Per a cada valor configurable, cridar `read_int_in_range()` per demanar un nou nombre
        dins de límits raonables (per exemple: alçada de la pala entre 60-160).
      - Recollir els cinc enters resultants i retornar-los plegats en l'ordre següent:
            (paddle_height, paddle_speed, ball_x_speed, ball_y_speed, ball_radius)

    Paràmetres
    ----------
    Cap

    Retorns
    -------
    int, int, int, int, int : 
        els valors de configuració seleccionats en l'ordre especificat ->
        paddle_height, paddle_speed, ball_x_speed, ball_y_speed, ball_radius

    Notes i consells
    ----------------
    - Usa `ask_yes_no(prompt)` per decidir si s'obre el menú.
    - Usa `read_int_in_range(prompt, low, high)` per llegir cada valor numèric.
    - Mantén la funció lliure d'assignacions globals: només ha de **retornar**
      els valors triats, no modificar constants.
    - Recorda mantenir el mateix ordre dels elements retornats.
    """
    # TODO: posa el teu codi!!!

    res_usuario = input("Vols canviar la configuració del joc?: ")
    # Es converteix la resposta en un valor booleà mitjançant la funció ask_si_no()
    cambiar_config = ask_si_no(res_usuario)

    if cambiar_config:
        # Es demana cada valor de configuració amb el seu rang corresponent
        paddle_height = read_int_in_range("Introdueix l'alçada de la pala (60-160 píxels) ", 60, 160)
        speed_paddle = read_int_in_range("Introdueix la velocitat de la pala (3-15 píxels per fotograma) ", 3, 15)
        speed_ball_x = read_int_in_range("Introdueix la velocitat X de la pilota (3-12 píxels per fotograma) ", 3, 12)
        speed_ball_y = read_int_in_range("Introdueix la velocitat Y de la pilota (3-12 píxels per fotograma) ", 3, 12)
        ball_radius = read_int_in_range("Introdueix el radi de la pilota (5-20 píxels): ", 5, 20)

        return paddle_height, speed_paddle, speed_ball_x, speed_ball_y, ball_radius    

    # Aquesta línia s'ha deixat perquè el programa complet funcioni
    # Correspon a l'usuari responent NO a canviar cap valor per defecte
    # L'hauràs d'eliminar quan afegeixis el teu codi
    return PADDLE_H, SPEED_PADDLE, SPEED_BALL_X, SPEED_BALL_Y, BALL_RADIUS 

def change_colors() -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """ Demana a l'usuari si vol modificar els colors del joc (fons i primer pla).

    Si l'usuari **no** vol canviar els colors, retorna les tuples per defecte:
        (BLACK, WHITE)

    Si l'usuari respon **sí**, la funció hauria de:
      - Demanar un nou color de **fons**.
      - Demanar un nou color de **primer pla** (el color utilitzat per a pales, pilota i text).
      - Cada color s'ha d'introduir com una tupla de tres enters
        que representen els components RGB (Vermell, Verd, Blau),
        amb cada valor entre 0 i 255.

    Paràmetres
    ----------
    Cap

    Retorns
    -------
    tuple[tuple[int, int, int], tuple[int, int, int]]
        Dues tuples de color RGB: (background_color, foreground_color)

    Notes i consells
    ---------------
    - Usa `ask_yes_no(prompt)` per decidir si s'obre la configuració de colors.
    - Usa `read_color(prompt)` per llegir un color cada vegada.
      Aquesta funció hauria de demanar per si mateixa els tres components RGB.
    - Recorda que els colors a pygame es defineixen com tuples de 3 enters: (vermell, verd, blau)
    - Mantén l'ordre dels valors retornats: primer fons, després primer pla.
    """

    # TODO: posa el teu codi!!!

    res_usuario = input("Vols canviar els colors del joc? ")
    # Es converteix la resposta en un valor booleà mitjançant la funció ask_si_no()
    cambiar_colores = ask_si_no(res_usuario)

    if cambiar_colores:
        # Es demana el color de fons mitjançant la funció read_color(),
        # que recull els tres valors RGB de manera controlada
        backg_col = read_color("fons")
        foreg_col = read_color("primer pla")
        return backg_col, foreg_col

    # Aquesta línia s'ha deixat perquè el programa complet funcioni
    # L'hauràs d'eliminar quan afegeixis el teu codi
    return BLACK, WHITE

def read_color(prompt: str) -> tuple[int, int, int]:
    """Demana a l'usuari que introdueixi els tres components RGB d'un color amb cada component a [0,255].
    La funció rep un text curt (per exemple: "fons" o "primer pla")
    que identifica quin color s'està configurant.

    Per a cadascun dels tres components — Vermell, Verd i Blau —
    la funció ha de demanar a l'usuari que introdueixi un enter entre 0 i 255
    (ambdós inclosos). Utilitza la funció d'ajuda `read_int_in_range()` per
    llegir de manera segura cada component.

    Paràmetres
    ----------
    prompt : str
        Una paraula que descrigui el color que es llegirà (p. ex. "fons", "primer pla").

    Retorns
    -------
   int, int, int
        Una tupla (r, g, b) que representa el color triat per l'usuari,
        on cada component és un enter dins del rang [0, 255].

    Notes i consells
    ---------------
    - Truca `read_int_in_range()` tres vegades, una per a cada component (Vermell, Verd, Blau).
    - Retorna els tres enters plegats com una sola tupla.
    - A pygame, els colors sempre s'expressen com tuples (R, G, B).
    - Mantén l'ordre (Vermell, després Verd, després Blau).
    """ 

    # TODO: posa el teu codi!!!

    print(f"Introdueix els components RGB per al color de {prompt}:")
    # Es llegeixen els tres components utilitzant la funció read_int_in_range()
    r = read_int_in_range("Component Vermell (0-255)", 0, 255)
    g = read_int_in_range("Component Verd (0-255)", 0, 255)
    b = read_int_in_range("Component Blau (0-255)", 0, 255)
    return (r, g, b)


def read_int_in_range(prompt: str, low: int, high: int) -> int:
    """Demana a l'usuari un enter dins de [low, high]. 
    Continua demanant fins que s'entra un valor vàlid.
    La implementació no ha d'aturar el programa per cap error.
    Hauria de ser robust a nombres fora de rang i entrades no enteres.

    Paràmetres
    ----------
    prompt : str
        El missatge que apareixerà abans que l'usuari escrigui l'entrada.
        Exemple: "Introdueix l'alçada de la pala".
    low : int
        El valor enter mínim permès.
    high : int
        El valor enter màxim permès.

    Retorns
    -------
    Un valor enter tal que low <= value <= high.
    """
    
    # TODO: posa el teu codi!!!
    print(f"{prompt}: ")
    while True:
        try:
            value = int(input())
            # Comprovem si el valor està dins del rang
            if low <= value <= high:
                return value
            else:
                print(f"Error: Si us plau, introdueix un enter entre {low} i {high}.")
        except ValueError:
            print("Error: Entrada invàlida. Si us plau, introdueix un nombre enter.")


    
def read_int_in_range_w_default(prompt: str, low: int, high: int, default_val: int) -> int:
    """ Versió avançada/alternativa més amigable de read_int_in_range().
    Funciona com la versió bàsica, però afegeix suport per a un *valor per defecte*.
    Pots fer-la com a substitut, però recomanem començar per la bàsica.

    Si l'usuari simplement prem ENTER sense escriure res,
    la funció retorna immediatament `default_val` **sense tornar a preguntar**.

    Resum del comportament:
      - Demana a l'usuari un enter dins del rang [low, high].
      - Si l'usuari introdueix un nombre vàlid, el retorna.
      - Si l'usuari prem directament ENTER, retorna `default_val`.
      - Si l'usuari introdueix text o un nombre fora de rang, imprimeix un missatge
        d'error i repeteix la pregunta.

    Paràmetres
    ----------
    prompt : str
        Missatge mostrat a l'usuari abans de l'entrada.
    low : int
        Valor enter mínim permès.
    high : int
        Valor enter màxim permès.
    default_val : int
        Valor retornat quan l'usuari prem ENTER sense escriure res.
        Ha d'estar dins del rang [low, high].
        Agafa el valor de la CONSTANT definida a l'inici

    Retorns
    -------
    int
        L'enter introduït per l'usuari, o `default_val` si ha premut ENTER.
    """
    
     # TODO: posa el teu codi!!!


def ask_si_no(prompt: str) -> bool:
    """ Formula una pregunta de sí/no a l'usuari i retorna el valor booleà corresponent.

    La funció hauria de demanar repetidament a l'usuari fins que es doni una resposta vàlida.
    Ha d'acceptar tant majúscules com minúscules i no ha de fallar amb text inesperat.

    Paràmetres
    ----------
    prompt : str
        La pregunta a mostrar a l'usuari (per exemple: "Canviar colors?").
        La funció hauria d'afegir "(s/n):" o una guia similar al prompt
        quan el mostri.

    Retorns
    -------
    bool
        True  → si l'usuari ha respost "s" o "si"
        False → si l'usuari ha respost "n" o "no"

    Notes i consells
    ---------------
    - Accepta formes curtes ("s", "n") i opcionalment paraules senceres ("si", "no").
    - Accepta també MAJÚSCULES, així que millor converteix l'entrada a minúscules
    - Imprimeix un missatge curt (p. ex. "Respon y/n, si us plau.") quan la resposta és invàlida.
    - Només retorna després de rebre una entrada vàlida; no aturis el programa amb errors.
    """
    # TODO: posa el teu codi!!!

    # Es normalitza la resposta de l'usuari a minúscules per facilitar la comparació
    if(str(prompt).lower() == "sí" or str(prompt).lower() == "si" or str(prompt).lower() == "s"):
        return True
    elif(str(prompt).lower() == "no" or str(prompt).lower() == "n"):
        return False
    else:
        print("Respon sí/s o no/n, siusplau")
        return ask_si_no(input("Vols canviar la configuració del joc?: "))


# ================================
# Funcions a completar: joc principal
# ================================

def move_paddle(current_y: int, direction: int, speed: int, height: int, paddle_h: int) -> int:
    """Retorna la nova coordenada y d'una pala, actualitzant la posició actual
    Paràmetres:
        current_y - posició superior actual de la pala (píxels)
        direction - direcció del moviment: -1 (amunt), 0 (quiet), +1 (avall)
        speed     - nombre de píxels a moure per fotograma (la velocitat sempre és positiva. Serà amunt o avall depenent de direction)
        height    - alçada del taulell
        paddle_h  - alçada de la pala
    Retorns:
        new_y     - posició y actualitzada (píxels)
    
    Tingues en compte que la pala ha de romandre sempre totalment visible en pantalla.
    És a dir, quan arriba als límits (amunt o avall) s'hi queda; considera aquí paddle_h i height.
    """
    # TODO: posa el teu codi!!!
    
    new_y = current_y + direction * speed

    if new_y < 0:
        new_y = 0
    elif new_y > height - paddle_h:
        new_y = height - paddle_h
    return new_y

    """
    Explicació de la nova y (new_y):"

        Amb aquest codi acabem de fer que els paddles es pugin moure usant una operació per crear constantment valors de new_y 
        Això ho hem aconseguit agafant la posició inicial del paddle (current_y) sumant-li constantment la direcció a partir dels inputs (a,z; up, down)
        Aquesta direcció la multipliquem per la velocitat (speed) per saber quant es mou per fotograma
    
    Explicació del límit del paddle:

        Si la nova posició sobrepassa el taulell per la part d'amunt fem que aquesta es quedi en la posició que estaba
        Per saber si la nova posició faría que el paddle sobrepassés el taulell per avall simplement hem de veure si la nova posició és mes gran que l'alçada del taulell - la alçada del paddle
        Si no es mou el paddle simplement retornaria la mateixa posició d'abans (current_y)
    """    


    # Aquesta línia s'ha deixat perquè el programa complet funcioni
    # L'hauràs d'eliminar quan afegeixis el teu codi
    return current_y


def move_ball(x: int, y: int, vx: int, vy: int) -> tuple[int, int]:
    """Mou la pilota un pas temporal. Retorna (x', y').
    Paràmetres:
        x  - posició horitzontal actual de la pilota (píxels)
        y  - posició vertical actual de la pilota (píxels)
        vx - velocitat horitzontal (increment de píxels a cada pas)
        vy - velocitat vertical (increment de píxels a cada pas)
    Retorns:
        new_x, new_y - posició horitzontal i vertical actualitzada (píxels)
    
    Tingues en compte que les col·lisions (és a dir, amb les pales, amb les parets) encara no es consideren aquí,
    sinó a les dues funcions següents (collide_ball_walls i collide_ball_paddle)
    """

    # TODO: posa el teu codi!!!

    

    new_x = x + vx
    new_y = y + vy


    # Aquesta línia s'ha deixat perquè el programa complet funcioni
    # L'hauràs d'eliminar quan afegeixis el teu codi
    return new_x, new_y


def collide_ball_walls(x: int, y: int, vx: int, vy: int, radius: int, width: int, height: int) -> tuple[int, int, int, int]:
    """Detecta i gestiona col·lisions amb les parets superior/inferior.
    Paràmetres:
        x       - posició horitzontal actual de la pilota (píxels)
        y       - posició vertical actual de la pilota (píxels)
        vx      - velocitat horitzontal (increment de píxels a cada pas)
        vy      - velocitat vertical (increment de píxels a cada pas)
        radius  - radi de la pilota (píxels)
        width   - amplada del taulell (píxels)
        height  - alçada del taulell (píxels)
    Retorns:
        x, y, vx, vy actualitzats
    Regles:
        Assegura't que la pilota es mantingui dins de l'àrea.
        No consideris els "gols" (quan la pilota toca les parets verticals) aquí. Comprova només els rebots horitzontals a les parets de dalt/baix
        En tocar una paret horitzontal, canvia el signe de vy
        Per detectar col·lisions amb precisió, potser cal considerar el radi de la pilota
    """
    # TODO: posa el teu codi!!!

    if y <= 0 or y + radius >= height:
        vy = -vy
    
    # Aquesta línia s'ha deixat perquè el programa complet funcioni
    # L'hauràs d'eliminar quan afegeixis el teu codi
    return x, y, vx, vy


def collide_ball_paddle(x: int, y: int, vx: int, vy: int,
                        paddle_x: int, paddle_y: int,
                        paddle_w: int, paddle_h: int,
                        radius: int) -> tuple[int, int, bool]:
    """
    Detecta i gestiona una col·lisió entre la pilota i una pala
    utilitzant una aproximació AABB (Axis-Aligned Bounding Box) senzilla.

    Paràmetres
    ----------
    x, y : Posició actual del CENTRE de la pilota (en píxels).
           Recorda: (0,0) és el cantó superior esquerre de la pantalla.
    vx, vy : Velocitats horitzontal i vertical actuals de la pilota (píxels per fotograma).
    paddle_x, paddle_y : Cantonada superior esquerra de la pala.
    paddle_w, paddle_h : Amplada i alçada de la pala.
    radius : Radi de la pilota.

    Retorns
    -------
    vx_new, vy_new : Velocitats possiblement modificades. vx s'inverteix si hi ha col·lisió.
    hit : True si s'ha produït una col·lisió, False altrament.

    Algoritme i consells
    -------------------
    1. Aproxima la pilota circular per un petit quadrat definit per:
           left   = x - radius
           right  = x + radius
           top    = y - radius
           bottom = y + radius
       Això simplifica les comprovacions: només rectangles.

    2. Compara aquesta "caixa de la pilota" amb el rectangle de la pala definit per:
           left   = paddle_x
           right  = paddle_x + paddle_w
           top    = paddle_y
           bottom = paddle_y + paddle_h
       Hi ha col·lisió quan els dos rectangles se superposen.

    3. Si se superposen:
         - Inverteix vx (velocitat horitzontal) per fer rebotar la pilota.
         - [OPCIONAL] Addicionalment (si la pilota a vegades queda "enganxada" a la pala), pots moure-la
           lleugerament fora de la pala per evitar-ho (experimenta!)
         - [OPCIONAL] També pots provar d'aplicar algun "efecte" fent que vy depengui una mica d'on
           la pilota colpeja la pala (experimenta!)

    Notes
    -----
    - Tant la pala com la pilota estan **alineades als eixos**, així que no cal trigonometria.
    - La caixa de col·lisió ignora la forma circular de la pilota per simplicitat,
      la qual cosa és suficient per a aquest joc.
    """
    # TODO: posa el teu codi!!!

    # Pala esquerra
    
    left_ball = x - radius
    right_ball = x + radius
    top_ball = y - radius
    bottom_ball = y + radius

    # Posicions de la pala
    left_paddle = paddle_x
    right_paddle = paddle_x + paddle_w
    top_paddle = paddle_y
    bottom_paddle = paddle_y + paddle_h

    # Inicialment no hi ha col·lisió
    hit = False

    # Comprovem superposició (AABB)
    if (right_ball >= left_paddle and
        left_ball <= right_paddle and
        bottom_ball >= top_paddle and
        top_ball <= bottom_paddle):
        vx = -vx       # Rebot horitzontal
        hit = True     # Marquem que hi ha hagut col·lisió

        # Opcional: podem moure la pilota fora de la pala per evitar que quedi enganxada
        if vx > 0:
            x = right_paddle + radius
        else:
            x = left_paddle - radius
    return vx, vy, hit

    # Aquesta línia s'ha deixat perquè el programa complet funcioni
    # L'hauràs d'eliminar quan afegeixis el teu codi
    

def reset_ball(center_x: int, center_y: int, vx0: int, vy0: int, to_right: bool) -> tuple[int, int, int, int]:
    """ Reinicia la pilota al centre de la pantalla i retorna la seva posició i velocitat inicials després d'haver-se marcat un punt.

    La pilota sempre ha de reiniciar des de les coordenades de centre donades per `center_x` i `center_y`, 
    però la seva direcció horitzontal depèn del paràmetre booleà `to_right`:
      - Si `to_right` és True  → la pilota es mou cap a la dreta.
      - Si `to_right` és False → la pilota es mou cap a l'esquerra.

    Es pot afegir una petita variació aleatòria a la velocitat vertical perquè el joc no es torni massa previsible.

    Paràmetres
    ----------
    center_x : int  - Coordenada x del centre de la pantalla (posició horitzontal inicial).
    center_y : int  - Coordenada y del centre de la pantalla (posició vertical inicial).
    vx0 : int       - Velocitat horitzontal base a utilitzar (nombre positiu).
    vy0 : int       - Velocitat vertical base a utilitzar (nombre positiu).
    to_right : bool - True si la pilota ha de començar anant cap a la dreta, False si cap a l'esquerra.

    Retorns
    -------
    x, y, vx, vy:
        x  nova posició horitzontal (centre)
        y  nova posició vertical (centre)
        vx velocitat horitzontal (el signe depèn de `to_right`)
        vy velocitat vertical (amb signe i/o magnitud possiblement aleatoritzats)

    Notes i consells
    ---------------
    - La funció no ha de dibuixar res, només calcular i retornar valors.
    - La posició inicial és sempre el centre de la pantalla.
    - La velocitat horitzontal ha d'apuntar en la direcció correcta segons `to_right`.
    - Opcionalment, aleatoritza lleugerament la velocitat vertical (p. ex., signe o magnitud) per donar variabilitat.
    """

    # TODO: posa el teu codi!!!
    
    x = center_x
    y = center_y

    if to_right:
        vx = vx0
    else:
        vx = -vx0
    
    vy_simbol = random.randint(-1, 1)

    if vy_simbol == 0:
        vy_simbol = 1 or -1

    vy = vy0 * vy_simbol


    # Aquesta línia s'ha deixat perquè el programa complet funcioni
    # L'hauràs d'eliminar quan afegeixis el teu codi
    return int(x), int(y), int(vx), int(vy)


def compute_ai_direction(ball_y: int, paddle_y: int, paddle_h: int) -> int:
    """ Computa la direcció de moviment (-1, 0, +1) per a una pala controlada per IA.
    L'objectiu és fer que la pala segueixi la pilota verticalment amb una reacció
    simple i limitada. La IA ha de moure la pala amunt, avall
    o deixar-la quieta segons la posició de la pilota relativa al
    centre de la pala.

    Paràmetres
    ----------
    ball_y : int
        La posició vertical actual de la pilota (centre de la pilota).
    paddle_y : int
        La posició vertical actual de la pala (vora superior).
    paddle_h : int
        L'alçada de la pala (per calcular-ne el centre).

    Retorns
    -------
    int
        -1 → moure amunt  
         0 → quedar-se quiet  
        +1 → moure avall
    
    Notes i consells
    ---------------
    La funció només ha de retornar la direcció, no actualitzar posicions.
    Et pot convenir usar una petita tolerància perquè la pala no “vibri”
    quan la pilota estigui prou alineada.
    """
    # TODO: posa el teu codi!!!
    
    center_paddle = paddle_y + paddle_h / 2

    tolerance = 10

    if ball_y < center_paddle - tolerance:  
        return -1
    elif ball_y > center_paddle + tolerance:
        return 1
    else:
        return 0

# =============================================
# LECTURA DE TELES AMUNT/AVALL (donat als estudiants)
# =============================================

def read_player_direction(keys, key_up: int, key_down: int) -> int:
    """Retorna -1, 0, o +1 segons les tecles premudes."""
    if keys[key_up]:
        return -1
    elif keys[key_down]:
        return 1
    return 0

# =================================
# Renderitzat (donat als estudiants)
# =================================

def draw_scene(screen: pygame.Surface,
               x: int, y: int,
               p1y: int, p2y: int,
               score_left: int, score_right: int,
               paddle_h: int, ball_radius: int,
               backg_col, foreg_col) -> None:
    
    screen.fill(backg_col)
    # línia central
    pygame.draw.line(screen, foreg_col, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 1)
    # pales
    pygame.draw.rect(screen, foreg_col, pygame.Rect(PADDLE_MARGIN, int(p1y), PADDLE_W, paddle_h))
    pygame.draw.rect(screen, foreg_col, pygame.Rect(WIDTH - PADDLE_MARGIN - PADDLE_W, int(p2y), PADDLE_W, paddle_h))
    # pilota
    pygame.draw.circle(screen, foreg_col, (int(x), int(y)), ball_radius)
    # marcador (simple)
    font = pygame.font.Font(None, 48)
    text = font.render(f"{score_left}   {score_right}", True, foreg_col)
    rect = text.get_rect(center=(WIDTH//2, 40))
    screen.blit(text, rect)
    pygame.display.flip()

def show_message(screen: pygame.Surface,message: str,backg_col, foreg_col, show_time_ms) -> None:
    """Mostra 'message' centrat a la pantalla del joc.
    Usat al final de la partida"""
    # Tria font i color del text
    font = pygame.font.Font(None, 96)     # font per defecte de pygame, mida 96
    text = font.render(message, True, foreg_col)

    # Centra el text al mig de la pantalla
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Omple la pantalla de fons i dibuixa el text
    screen.fill(backg_col)
    screen.blit(text, rect)
    pygame.display.flip()

    # Pausa perquè els jugadors ho puguin veure
    pygame.time.wait(show_time_ms)

# =================================
# Bucle principal (donat als estudiants)
# =================================

def main() -> None:

    global play_against_machine

    paddle_h, paddle_speed, speed_ball_x, speed_ball_y, ball_radius = get_config()
    backg_col, foreg_col = change_colors()

    mode = input("Vols jugar contra l'ordinador? (s/n): ").strip().lower()
    play_against_machine = ask_si_no(mode)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laboratori 2 - Pong")
    clock = pygame.time.Clock()

    # Estat inicial (sense llistes ni objectes)
    p1_y = (HEIGHT - paddle_h) / 2
    p2_y = (HEIGHT - paddle_h) / 2
    ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=True)

    score_left = 0
    score_right = 0

    running = True

    while running:
        # 1) Esdeveniments (tancar finestra + entrada)
        direction_left = 0
        direction_right = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        # La pala esquerra sempre és humana
        direction_left = read_player_direction(keys, KEY_UP_LEFT, KEY_DOWN_LEFT)
        # La pala dreta pot ser humana o IA
        if play_against_machine:
            direction_right = compute_ai_direction(ball_y, p2_y, PADDLE_H)
        else:
            direction_right = read_player_direction(keys, KEY_UP_RIGHT, KEY_DOWN_RIGHT)

        # 2) Actualitza estat (NOMÉS cridant funcions)
        p1_y = move_paddle(p1_y, direction_left, SPEED_PADDLE, HEIGHT, paddle_h)
        p2_y = move_paddle(p2_y, direction_right, SPEED_PADDLE, HEIGHT, paddle_h)

        ball_x, ball_y = move_ball(ball_x, ball_y, ball_vx, ball_vy)
        ball_x, ball_y, ball_vx, ball_vy = collide_ball_walls(ball_x, ball_y, ball_vx, ball_vy, ball_radius, WIDTH, HEIGHT)

        # Col·lisió amb la pala esquerra
        vx_tmp, vy_tmp, hit_left = collide_ball_paddle(
            ball_x, ball_y, ball_vx, ball_vy,
            PADDLE_MARGIN, p1_y, PADDLE_W, paddle_h, ball_radius)
        if hit_left:
            ball_vx, ball_vy = vx_tmp, vy_tmp

        # Col·lisió amb la pala dreta
        vx_tmp, vy_tmp, hit_right = collide_ball_paddle(
            ball_x, ball_y, ball_vx, ball_vy,
            WIDTH - PADDLE_MARGIN - PADDLE_W, p2_y, PADDLE_W, paddle_h, ball_radius)
        if hit_right:
            ball_vx, ball_vy = vx_tmp, vy_tmp

        # 3) Puntuació (si la pilota surt de la pantalla): reinicia pilota
        if ball_x < -ball_radius:
            score_right += 1
            pygame.time.wait(SERVE_PAUSE)  # petita pausa abans de tornar a treure
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=True)
        elif ball_x > WIDTH + ball_radius:
            score_left += 1
            pygame.time.wait(SERVE_PAUSE)  # petita pausa abans de tornar a treure
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=False)
        
        if score_left == POINTS_END or score_right == POINTS_END:
            show_message(screen,"Fi de la partida!",backg_col, foreg_col,2000)
            running = False

        # 4) Renderitza
        draw_scene(screen, ball_x, ball_y, p1_y, p2_y, score_left, score_right, 
                   paddle_h, ball_radius, backg_col, foreg_col)

        clock.tick(FPS)

    # sortint del bucle principal
    pygame.quit()
    sys.exit(0)   # Garanteix una sortida completa i neta del programa (evita processos penjats)

# NOTA AVANÇADA:
# Les 2 línies següents inicien el programa cridant la funció main()
# Quan executes: python pong3.py, Python estableix una variable incorporada: __name__ = "__main__"
# Així la condició s'assegura que aquesta funció main() s'executa només quan executes aquest fitxer directament,
# i no quan s'importa des d'un altre fitxer.
if __name__ == "__main__":
    main()
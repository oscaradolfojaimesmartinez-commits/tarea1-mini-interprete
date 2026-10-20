# Análisis — Tarea 1

**Integrantes:**
1. Oscar Adolfo Jaimez Martinez
2.
3.

**Fork:** https://github.com/oscaradolfojaimesmartinez-commits/tarea1-mini-interprete/pull/1 

**Rama:** tarea1-pruebas-refactorizacion

> Contesten en este archivo. Respuestas breves y concretas: se califica que
> hayan entendido, no la extensión.

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` | Un texto (`str`) | Una lista de `Token` (tipo, valor, posición) | Partir el texto en piezas: ignora espacios, junta dígitos en un número y reconoce los símbolos. Rechaza los caracteres que no conoce. No sabe nada de precedencia ni de estructura. |
| `parser` | La lista de tokens | La raíz del AST | La estructura: precedencia (`*` y `/` antes que `+` y `-`), asociatividad a la izquierda y paréntesis. Rechaza expresiones mal formadas. No calcula nada. |
| `ast` | No recibe ni entrega: son las clases `Numero` y `OperacionBinaria` | El árbol que arma el parser | Representar cómo quedó agrupada la expresión. Son solo datos, sin lógica de cálculo. |
| `evaluator` | La raíz del AST | Un número (`int` o `float`) | Calcular el valor recorriendo el árbol de abajo hacia arriba. Reporta la división entre cero como `ErrorDeEvaluacion`. |

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

| Etapa | Cómo se ve `(3 + 4) * 2` aquí |
|---|---|
| texto | `"(3 + 4) * 2"` |
| tokens | `[PAR_IZQ '(' @0, NUMERO 3 @1, MAS '+' @3, NUMERO 4 @5, PAR_DER ')' @6, POR '*' @8, NUMERO 2 @10]` |
| AST | `OperacionBinaria('*', OperacionBinaria('+', Numero(3), Numero(4)), Numero(2))`, que con `--arbol` se ve así: |
| resultado | `14` |

```
*
|-- +
|   |-- 3
|   `-- 4
`-- 2
```

La suma quedó adentro porque los paréntesis la fuerzan a armarse primero, y la
multiplicación queda como raíz. El evaluator calcula primero `3 + 4 = 7` y
luego `7 * 2 = 14`. Comprobé el dibujo con `python3 interprete.py --arbol "(3 + 4) * 2"`.

---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
| `test_evaluator::test_suma` | evaluator | `3 + 4` da 7 | 1 (`+`) | Normal |
| `test_evaluator::test_resta` | evaluator | `10 - 3` da 7 | 1 (`-`) | Normal |
| `test_evaluator::test_multiplicacion` | evaluator | `6 * 7` da 42 | 1 (`*`) | Normal |
| `test_evaluator::test_division` | evaluator | `10 / 2` da 5 | 1 (`/`) | Normal |
| `test_evaluator::test_precedencia_sin_parentesis` | evaluator | `3 + 4 * 2` da 11 | 2 (`+`, `*`) | Normal |
| `test_evaluator::test_precedencia_con_parentesis` | evaluator | `(3 + 4) * 2` da 14 | 2 (`+`, `*`) | Normal |
| `test_lexer::test_tokeniza_un_numero_solo` | lexer | `42` produce un solo token `NUMERO` con su posición | 0 | Frontera (entrada mínima) |
| `test_lexer::test_tokeniza_una_suma` | lexer | `3+4` produce tres tokens con sus posiciones | 1 (`+`) | Normal |
| `test_lexer::test_los_espacios_no_producen_tokens` | lexer | `"  3   +   4  "` produce solo 3 tokens | 1 (`+`) | Frontera (espacios) |
| `test_lexer::test_tokeniza_parentesis` | lexer | `(3)` produce `PAR_IZQ`, `NUMERO`, `PAR_DER` | 0 | Normal |
| `test_parser::test_construye_el_arbol_de_una_suma` | parser | `3 + 4` forma una `OperacionBinaria('+')` | 1 (`+`) | Normal |
| `test_parser::test_la_multiplicacion_se_agrupa_antes_que_la_suma` | parser | `3 + 4 * 2` se agrupa como `3 + (4 * 2)` | 2 (`+`, `*`) | Normal |
| `test_parser::test_los_parentesis_cambian_la_agrupacion` | parser | `(3 + 4) * 2` se agrupa al revés | 2 (`+`, `*`) | Normal |

Leída como columna: **ninguna prueba es inválida**, ninguna usa dos operadores
de la misma precedencia seguidos, y las que usan dos operadores siempre son
`+` con `*`.

### 2.2 ¿Qué comportamientos **no** estaban probados?

- **Entradas inválidas**: no había ninguna prueba de que algo se rechace (`3 +`,
  `(3 + 4`, `3 4`, `3 + 4)`, vacío, `-3`, caracteres como `$`).
- **Asociatividad a la izquierda**: nada encadenaba operadores de la misma
  precedencia (`10 - 3 - 2`, `8 / 4 / 2`). Ahí estaba el defecto principal.
- **División entre cero**: la semántica pide `ErrorDeEvaluacion` y no se probaba.
- **Tipo del resultado de la división**: `test_division` compara contra `5`,
  y `5 == 5.0` en Python, así que no distingue si devuelve `int` o `float`.
- **Ceros a la izquierda** (`007`), **paréntesis anidados** y **entrada vacía**.
- **Posición en los mensajes de error**: nada la verificaba.
- **Caracteres desconocidos en el lexer**: solo se probaban entradas válidas.
- **Pendiente que no se resolvió**: `ErrorDeEvaluacion` (la división entre cero)
  no lleva posición, aunque la semántica pide que los mensajes de error la
  indiquen. Los nodos del AST no guardan posición, así que arreglarlo
  requeriría un cambio más grande. Queda como limitación conocida.

---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

Todas están en `tests/test_casos_nuevos.py`.

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
|---|---|---|---|---|
| `test_multiplicacion_antes_de_la_suma_a_la_izquierda` | `2 * 3 + 4` | 10 | Normal | Expresión típica; el `*` va a la izquierda del `+`, al revés que en las pruebas originales |
| `test_parentesis_anidados` | `((1 + 2) * (3 + 4))` | 21 | Normal | Uso ordinario de paréntesis, con dos grupos dentro de uno |
| `test_resta_encadenada` | `10 - 3 - 2` | 5 | Normal | Encadenar dos restas es uso común; revela el defecto de asociatividad |
| `test_division_encadenada` | `8 / 4 / 2` | 1.0 | Normal | Mismo defecto, con división |
| `test_multiplicacion_y_division_encadenadas` | `12 / 3 * 2` | 8.0 | Normal | Mismo nivel de precedencia con operadores distintos |
| `test_ceros_a_la_izquierda` | `007` | 7 | Frontera | La semántica dice que `007` es 7; es el límite de cómo se lee un número |
| `test_division_es_real` | `10 / 4` | 2.5 | Frontera | La división no es entera; es el caso donde un entero daría 2 |
| `test_division_exacta_regresa_flotante` | `10 / 2` | 5.0 (`float`) | Frontera | División exacta: debe seguir siendo `float` |
| `test_espacios_en_cualquier_cantidad` | `"   3     +   4   "` | 7 | Frontera | Espacios al inicio, al final y de sobra |
| `test_division_entre_cero` | `10 / 0` | `ErrorDeEvaluacion` | Frontera | El divisor en el valor límite (0) |
| `test_division_entre_cero_disfrazada` | `1 / (2 - 2)` | `ErrorDeEvaluacion` | Frontera | El cero aparece al evaluar, no como literal |
| `test_operador_sin_operando_derecho` | `3 +` | `ErrorDeSintaxis` | Inválida | Falta el operando derecho |
| `test_parentesis_sin_cerrar` | `(3 + 4` | `ErrorDeSintaxis` | Inválida | Falta el `)` |
| `test_parentesis_de_mas_al_final` | `3 + 4)` | `ErrorDeSintaxis` | Inválida | Sobra un `)` |
| `test_dos_numeros_seguidos` | `3 4` | `ErrorDeSintaxis` | Inválida | Dos números sin operador |
| `test_entrada_vacia` | `""` | `ErrorDeSintaxis` | Inválida | No hay expresión |
| `test_menos_unario_no_se_soporta` | `-3` | `ErrorDeSintaxis` | Inválida | La semántica declara que el menos unario no se soporta |
| `test_caracter_desconocido` | `3 $ 4` | `ErrorDeSintaxis` | Inválida | `$` no es parte del lenguaje |
| `test_el_error_indica_la_posicion` | `3 + * 4` | `ErrorDeSintaxis` con `posicion == 4` | Inválida | Verifica que el error señale el lugar, como pide la semántica |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

La **asociatividad**: `10 - 3 - 2` daba `9` y `8 / 4 / 2` daba `4.0`.

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

La semántica declarada del README (sección 7, fila "Asociatividad") dice que
los operadores de la misma precedencia se asocian **a la izquierda**. Entonces
`10 - 3 - 2` debe ser `(10 - 3) - 2 = 5`, y no `10 - (3 - 2) = 9`.

El parser original asociaba a la derecha porque `_expresion` se llamaba a sí
misma para armar el lado derecho: `10 - 3 - 2` quedaba como `10 - (3 - 2)`.
`_termino` hacía lo mismo con `*` y `/`.

Las otras fallas violaban otras filas de la semántica ("Entrada inválida debe
rechazarse con ErrorDeSintaxis, nunca con un error de Python"):
- `3 +`, `(3 + 4` y la entrada vacía lanzaban `IndexError`.
- `3 4` y `3 + 4)` se aceptaban y daban un resultado.
- `3 $ 4` se aceptaba porque el lexer ignoraba en silencio el `$`.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| Asociatividad a la derecha | `10 - 3 - 2` | `9` | `5` | `0955252` | `ac7bd8a` |
| Asociatividad a la derecha | `8 / 4 / 2` | `4.0` | `1.0` | `0955252` | `ac7bd8a` |
| Asociatividad a la derecha | `12 / 3 * 2` | `2.0` | `8.0` | `0955252` | `ac7bd8a` |
| Fin de entrada inesperado | `3 +`, `(3 + 4`, `""` | `IndexError` | `ErrorDeSintaxis` | `0955252` | `ac7bd8a` |
| Tokens sobrantes sin revisar | `3 4`, `3 + 4)` | un resultado (`3` y `7`) | `ErrorDeSintaxis` | `0955252` | `ac7bd8a` |
| Caracter desconocido ignorado | `3 $ 4` | un resultado (`3`) | `ErrorDeSintaxis` | `0955252` | `9ea2095` |

Cambios concretos: en el parser, `_expresion` y `_termino` pasaron de recursión
a un ciclo `while`; `parsear()` ahora revisa que no sobren tokens; y
`_avanzar()` lanza `ErrorDeSintaxis` si se acaban los tokens. En el lexer, el
`else` final lanza `ErrorDeSintaxis` en lugar de avanzar en silencio.

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

- Las pruebas de asociatividad usan tres cadenas distintas (`-`, `/`, y
  `/` con `*`), no un solo ejemplo.
- La corrección no trata casos particulares: el ciclo `while` aplica la misma
  regla a cualquier operador de ese nivel y a cualquier longitud de cadena.
  Cada vuelta toma lo acumulado como lado izquierdo, que es la definición de
  asociar a la izquierda.
- Para las entradas inválidas, la revisión de tokens sobrantes y de fin de
  entrada está en `parsear()` y en `_avanzar()`, o sea, en el punto por donde
  pasa toda entrada, y no depende de qué expresión sea.
- Las 13 pruebas originales siguen pasando (32 en total).

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?

1. **Duplicación** en el parser: `_expresion` y `_termino` eran el mismo código
   con dos diferencias (qué operadores aceptan y a qué método llaman después).
   El defecto de asociatividad estaba duplicado también: aparecía en las dos.
   Arreglarlo en una sola habría dejado el defecto en la otra.
2. **Condicionales repetidos** en el evaluator: un `if` por cada operador, con
   la misma estructura, más el manejo especial de la división dentro del último.
3. **Rigidez / amplificación del cambio**: agregar un operador obliga a tocar
   varios archivos, porque el conocimiento de qué operadores existen está
   repartido entre el lexer, los tokens, el parser y el evaluator.
4. **Duplicación en `cli.py`**: el recorrido `Parser(tokenizar(texto)).parsear()`
   aparece en `interpretar` y otra vez en `_una_expresion` (la rama de `--arbol`).
   No la refactoricé.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

**Parser.** Extraje `_binaria(operadores, siguiente_nivel)`. Los dos ciclos
tenían exactamente la misma forma y solo cambiaban dos cosas: el conjunto de
operadores y el método del nivel siguiente. Al convertirlas en parámetros,
`_expresion` y `_termino` quedan en una línea cada una. Es equivalente porque
construye el mismo AST: mismos nodos, mismo orden y misma asociatividad.

**Evaluator.** Cambié la cadena de `if` por una tabla `OPERACIONES` que asocia
cada símbolo con su función (`operator.add`, `operator.sub`, `operator.mul` y
`_dividir`). Es equivalente porque cada operador ejecuta la misma operación que
antes; la revisión de división entre cero quedó dentro de `_dividir`, así que
solo aplica a `/` como antes; y un operador que no está en la tabla sigue
lanzando `ErrorDeEvaluacion("operador desconocido")`.

Además de que las 32 pruebas siguen pasando, no cambié ninguna prueba para lograrlo.

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

**Ninguno.**

- **Factory Method** sirve cuando hay que decidir qué clase concreta crear y
  esa decisión crece o varía. Aquí solo hay dos tipos de nodo, y
  `OperacionBinaria` se crea en un único lugar (`_binaria`). La tabla
  `OPERACIONES` ya resuelve "qué hacer según el operador" sin clases nuevas.
- **Adapter** sirve para hacer compatible una interfaz ajena con la que
  esperamos. Aquí todos los componentes son propios y encajan entre sí; no hay
  ninguna interfaz externa que adaptar.
- Agregar uno de los dos solo sumaría clases sin mejorar nada.

Para que empezara a convenir tendría que cambiar el sistema. Un Factory Method
tendría sentido si hubiera muchas clases de nodo (unarios, funciones,
variables) y el parser tuviera que decidir cuál crear. Un Adapter tendría
sentido si tuviéramos que usar un lexer o un evaluador externo con otra interfaz.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

Para agregar `%` hay que tocar **4 archivos**:
1. `tokens.py`: un nuevo `TipoToken`.
2. `lexer.py`: añadir el símbolo en `SIMBOLOS`.
3. `parser.py`: incluir el token en `OPERADORES_PRODUCTO` (o en el nivel que corresponda).
4. `evaluator.py`: una entrada en `OPERACIONES`.

Es lo más difícil de modificar porque la lista de operadores no está en un
solo lugar: cada etapa tiene su propia versión, y se enlazan por un símbolo
escrito como cadena (`"%"`). Si se olvida uno de los cuatro, el fallo es
silencioso o aparece lejos. Antes del refactor del evaluator eran los mismos 4
archivos, pero el cambio en el evaluator era más grande (un `if` nuevo, con su
propio manejo).

---

## Antes de la declaración: inténtenlo primero ustedes

Usar IA o no es decisión de cada quien, y el curso la permite. Pero **les
pedimos, por favor, que primero hagan el análisis por su cuenta.**

No es una prueba de honestidad. Es que el orden cambia lo que aprenden:

1. **Primero ustedes.** Lean el código, corran las pruebas, escriban sus
   respuestas. Aunque queden incompletas, aunque no encuentren todo.

2. **Después, si quieren, la IA** — pero como contraste, no como sustituto.
   Y entonces contesten dos preguntas, en `DECLARACION_IA.md`:

   - **¿Qué encontró que ustedes no habían notado?**
     Eso es aprendizaje, y se declara sin ninguna pena.

   - **¿Qué *no* encontró, que en este curso sí consideramos un problema?**
     Ésta es la interesante. Una herramienta suele decir que el código
     "funciona bien" y no señalar, por ejemplo, la **duplicación** — porque
     duplicar no rompe nada, el programa corre igual. Pero ustedes ya saben
     por qué eso sí es un mal diseño, y saben nombrarlo. La herramienta no
     tomó esa clase.

> Si invierten el orden se pierden justamente lo segundo: **no se puede notar
> lo que a una herramienta le faltó si uno nunca se formó una opinión propia
> antes de preguntarle.** Y que un programa funcione no implica que esté bien
> diseñado — eso lo dijimos en clase mucho antes de esta tarea.

---

## Declaración de uso de Inteligencia Artificial

Va en `DECLARACION_IA.md`, no aquí. Es obligatoria, pero **no da ni quita
puntos**: es un reporte adicional que se revisa aparte y se les devuelve con
comentarios.

**No se evalúa cuánta IA usaron.** Se evalúa si pueden dar cuenta de lo que
entregaron. *"No usamos"* es una declaración válida y completa; *"lo
descartamos porque..."* es de las mejores respuestas posibles.
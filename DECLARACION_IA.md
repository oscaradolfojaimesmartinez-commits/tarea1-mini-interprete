# Declaración de uso de Inteligencia Artificial

**Actividad:** Tarea 1 — Mini intérprete de expresiones (Modelado y Programación)

**Integrantes:** Oscar Adolfo Jaimez Martinez

**Fecha:** 19 de octubre de 2026

> Esta declaración es obligatoria en toda tarea, práctica y en el proyecto final.
> **No da ni quita puntos**: es un reporte adicional que se revisa aparte y se
> devuelve con comentarios. **No se evalúa cuánta IA usaron**, sino si pueden
> dar cuenta de lo que entregaron.

---

## 0. ¿Se usó IA en esta actividad?

- [ ] **No.** Firmen la última sección y terminen. Con eso queda completa.
- [x] **Sí.** Contesten los cinco puntos.

---

## 1. Herramienta(s) utilizada(s)

| Herramienta | Versión o modelo, si lo saben |
|---|---|
| Claude (Anthropic) | Claude Sonnet 5.5, según la interfaz |

---

## 2. Objetivo del uso

| Para qué la usamos | En qué parte del entregable |
|---|---|
| Entender qué pide la tarea (el PDF del README) y planear los pasos | Todo el trabajo |
| Guiar la instalación y la configuración de Git, el fork y el venv | Ambiente de trabajo |
| Leer el código del proyecto y encontrar defectos|   Pruebas |
| Ayuda con la estructura de los .md | Analisis y DECLARACION_IA| 

---

## 3. Prompts principales

Textuales, tal como los escribieron. No los limpien ni los reescriban.

```
TENGO QUE HACER ESA TAREA
```
(Con el PDF del README del repositorio adjunto.)

```
COMO PUEDO PASARTELOS DE UNA?? COMPRIMIDO?? O COMO ES QUE SON MUCHOS
```

```
primero ayudame a extraer todo a mi lap
```

```
aver empecemos desde el inicio..
```

```
aver antes de hacer eso... que es lo que realmente tengo que hacer??
que es lo que me estan pidiendo hacer...
```

```
Que otras pruebas podemos agregar
```

```
Donde mas puede quebrar
```

```
No le entiendo a lexer
```

```
Como pongo un salto de linea en una tabla
```

```
Como se agrega una tabla
```





Además pegué en la conversación la salida de la terminal en varios pasos
(`pytest`, `git diff`, `git log`, `git status`) y capturas de pantalla del
explorador de archivos y de la página del Pull Request, para que la
herramienta pudiera guiar el siguiente paso.

---

## 4. Cómo se incorporó o se descartó lo obtenido

**Éste es el punto que más pesa.**

| Qué produjo la herramienta | ¿Aceptado, modificado o descartado? | Por qué | Dónde quedó (archivo / commit) |
|---|---|---|---|
| Archivo de pruebas nuevas | Modificado | Al correrlas contra el código original fallaron  4 | `tests/test_casos_nuevos.py`, commit `0955252` (el mensaje del commit lo corregí yo, quité una palabra) |
| Ayuda con lexer (rechazar caracteres desconocidos) | Aceptado sin cambios | El `git diff` mostró solo el `import` y el `else`, y quedaron 8 fallas en lugar de 9 | `lexer.py`, commit `9ea2095` |


### 4.1 Si la usaron para el análisis: el contraste

Se les pidió intentarlo primero por su cuenta. Si lo hicieron así:

| | |
|---|---|
| ¿Qué encontró la herramienta que ustedes **no** habían notado? | El parser asociaba a la derecha porque `expresion` y `termino` se llamaban a sí mismas; el lexer ignoraba en silencio los caracteres desconocidos; y parsear() no revisaba si sobraban tokens. |
| ¿Qué **no** encontró, que en este curso sí consideramos un problema? | Las pruebas del evaluator pasan por interpretar, así que prueban lexer, parser y evaluator juntos (acoplamiento: si falla una, no se sabe qué componente fue). Mis pruebas nuevas hacen lo mismo. La duplicación en `cli.py` y la falta de posición en `ErrorDeEvaluacion` solo salieron al escribir el análisis, y quedaron sin resolver. `main` ignora el código de retorno de `_una_expresion` en modo interactivo. |

> Si no usaron IA para el análisis, escriban *"no aplica"*.

### 4.2 ¿Cómo verificaron que lo que incorporaron era correcto?

- Corrí `pytest` después de cada paso y comparé el resultado con el que se
  anunció: 9 failed / 23 passed con las pruebas nuevas; 8 / 24 tras el lexer;
  32 passed tras el parser, tras `_binaria` y tras el evaluator.
- Leí el `git diff` de cada archivo antes de hacer commit, para confirmar que
  el cambio era el esperado y no tocaba otras cosas.
- No modifiqué ni borré ninguna de las 13 pruebas originales; siguen pasando.
- Probé a mano entradas como `10 - 3 - 2` con `python3 interprete.py` y vi que daba `5`. [También comprobé el AST de `(3 + 4) * 2` con `--arbol` y comparé con mi dibujo, si lo hiciste]

---

## 5. Reflexión

### 5.1 ¿Qué limitación concreta observaron **en esta actividad**?

- La herramienta no pudo ejecutar `pytest` en su entorno (no estaba instalado)
  y verificó sus cambios con un corredor improvisado. La verificación real fue
  la mía, en mi máquina.
- Anunció que quedarían 6 pruebas fallando después del lexer y eran 8; lo
  corrigió después de ver mi salida.
- Solo vio el código por un `.zip` y el PDF del README, donde algunos nombres
  salían traducidos (`requisitos.txt`, `interpretar.py`), así que sus
  indicaciones iniciales usaron nombres que no eran los reales de los archivos.


### 5.2 ¿Qué harían distinto la próxima vez?

Hacer primero el análisis por
mi cuenta, leyendo el código y escribiendo mis respuestas aunque quedaran
incompletas, y usar la herramienta después, como contraste; empezar antes del
día de la entrega.

---

## Firma

> Declaramos que entendemos y podemos explicar todo lo que entregamos,
> independientemente de las herramientas que hayamos utilizado.

| Nombre | Número de cuenta |
|---|---|
| Oscar Adolfo Jaimez Martinez | 322156120 |
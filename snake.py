#coding: utf-8
import os
import random
import curses
from curses import wrapper

# Atualiza a velocidade da cobra
def updateScr(time):
	time = time - 1
	if time > 10:
		return time
	else:
		return 10

# Desenha as paredes do mapa
def drawWalls(w, sw, sh):
	for i in range(sh-1):
		for j in range(sw):
			if (i == 0 and j < sw-1) or i == sh-2:
				wall = [i, j]
				w.addch(wall[0], wall[1], curses.ACS_CKBOARD)
			if (j == 0) or (j == sw-2 and i < sh-1):
				wall = [i, j]
				w.addch(wall[0], wall[1], curses.ACS_CKBOARD)
			wall = [sh-2, sw-1]
			w.addch(wall[0], wall[1], curses.ACS_DEGREE)


def game():
	# Inicializa a tela e seta o cursor fora da tela
	s = curses.initscr()				
	curses.curs_set(0)

	# Guarda altura e largura da tela
	sh, sw = s.getmaxyx()

	# Cria uma nova tela usando as coordenadas obtidas e inicialiada em (0, 0)				
	w = curses.newwin(sh, sw, 0, 0)

	# Habilita o uso do teclado e atualiza a tela a cada 100ms
	w.keypad(1)		
	time = 100
	time = updateScr(time)
	w.timeout(time)

	drawWalls(w, sw, sh)

	# Define a posicao inicial da cobra
	snakeX = sw / 4
	snakeY = sh / 2

	# Seta as 3 partes da cobra
	snake = [
		[snakeY, snakeX],
		[snakeY, snakeX - 1],
		[snakeY, snakeX - 2]
	]

	# Define a posicao inicial da comida
	food = [sh / 2, sw / 2]
	w.addch(food[0], food[1], curses.ACS_DIAMOND)

	# Cobra inicia movimentando pra direita
	key = curses.KEY_RIGHT

	while True:
		# Captura a proxima tecla pressionada
		nextKey = w.getch()
		key = key if nextKey == -1 else nextKey

		# Limites do mapa, caso o usuário caia fora, encerra o jogo
		if snake[0][0] in [0, sh] or snake[1][1] in [sw, sw-2] or snake[0][0] in [sh-2, sh-2] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
			gameOverScreen()
			exit()

		# Nova cabeça da cobra
		newHead = [
			snake[0][0], snake[0][1]
		]

		# Movimentação da cobra
		if key == curses.KEY_UP:
			newHead[0] -= 1
		if key == curses.KEY_DOWN:
			newHead[0] += 1
		if key == curses.KEY_LEFT:
			newHead[1] -= 1
		if key == curses.KEY_RIGHT:
			newHead[1] += 1

		# Insere nova parte da cobra
		snake.insert(0, newHead)

		# Caso a cobra tenha se alimentado, gera um novo alimento em local aleatório
		if snake[0] == food:
			time = updateScr(time)
			w.timeout(time)
			food = None
			while food is None:
				nf = [
					random.randint(2, sh - 3),
					random.randint(2, sw - 3)
				]
				food = nf if nf not in snake else None

			w.addch(food[0], food[1], curses.ACS_DIAMOND)
		else:
			tail = snake.pop()
			w.addch(tail[0], tail[1], ' ')

		# Desenha a cobra
		w.addch(snake[0][0], snake[0][1], curses.ACS_BLOCK)

# Tela inicial do game
def mainMenu():
	stdscr = curses.initscr()
	curses.noecho()
	stdscr.keypad(True)

	# Guarda altura e largura da tela
	sh, sw = stdscr.getmaxyx()

	# Cria uma nova tela usando as coordenadas obtidas e inicialiada em (0, 0)				
	w = curses.newwin(sh, sw, 0, 0)

	# Imprime o menu inicial na tela
	stdscr.addstr( '-------------------------------------------------------------------------------\n')
	stdscr.addstr( '                0000000   0000    00  0000000  00   00  0000000\n')
	stdscr.addstr( '                0000000   0000    00  0000000  00  00   0000000\n')
	stdscr.addstr( '                000       00 00   00  00   00  00 00    00\n')
	stdscr.addstr( '                0000000   00  00  00  00   00  0000     0000000\n')
	stdscr.addstr( '                    000   00   00 00  0000000  00 00    00\n')
	stdscr.addstr( '                0000000   00    0000  00   00  00  00   0000000\n')
	stdscr.addstr( '                0000000   00     000  00   00  00   00  0000000\n')
	stdscr.addstr( '-------------------------------------------------------------------------------\n')
	stdscr.addstr( '                   Programmed by LeoBissani - Version 1.0.0\n')
	stdscr.addstr( '-------------------------------------------------------------------------------\n')
	stdscr.addstr( ' \n')

	stdscr.addstr("                               Resolution = ")
	stdscr.addstr(format(sw))
	stdscr.addstr("x")
	stdscr.addstr(format(sh))
	stdscr.addstr( ' \n \n \n \n')
	stdscr.addstr( '                            Press any key to start...\n')
	stdscr.getch()

# Tela de game over do jogo
def gameOverScreen():
	stdscr = curses.initscr()
	stdscr.clear()
	curses.noecho()
	stdscr.keypad(False)

	# Guarda altura e largura da tela
	sh, sw = stdscr.getmaxyx()

	# Cria uma nova tela usando as coordenadas obtidas e inicialiada em (0, 0)				
	w = curses.newwin(sh, sw, 0, 0)

	# Imprime na tela a mensagem de game over
	stdscr.addstr( ' \n \n')
	stdscr.addstr( '-------------------------------------------------------------------------------\n')
	stdscr.addstr( '                0000000  0000000  000         000  0000000\n')
	stdscr.addstr( '                0000000  0000000  0000       0000  0000000\n')
	stdscr.addstr( '                000      00   00  00000     00000  00\n')
	stdscr.addstr( '                000 000  00   00  000000   000000  0000000\n')
	stdscr.addstr( '                000  00  0000000  000  00000  000  00\n')
	stdscr.addstr( '                0000000  00   00  000   000   000  0000000\n')
	stdscr.addstr( '                0000000  00   00  000    0    000  0000000\n')
	stdscr.addstr( ' \n \n \n')
	stdscr.addstr( '                   0000000  00      00  0000000  0000000\n')
	stdscr.addstr( '                   0000000  00      00  0000000  0000000\n')
	stdscr.addstr( '                   00   00  00      00  00       000  00\n')
	stdscr.addstr( '                   00   00   00    00   0000000  000  0\n')
	stdscr.addstr( '                   00   00    00  00    00       00000\n')
	stdscr.addstr( '                   0000000     0000     0000000  000 000\n')
	stdscr.addstr( '                   0000000      00      0000000  000  000\n')
	stdscr.addstr( '-------------------------------------------------------------------------------\n')
	stdscr.addstr( ' \n')

	# Espera pelo input do usuário
	stdscr.getch()

	# Limpa a tela e finaliza
	w.refresh()
	os.system("clear")
	curses.endwin()
	exit()

mainMenu()
game()
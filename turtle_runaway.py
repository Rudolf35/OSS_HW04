# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, myturtle, catch_radius=20):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.myturtle = myturtle
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()
        
        self.myturtle.shape('turtle')
        self.myturtle.color('green')
        self.myturtle.penup()
        
        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        r = self.myturtle.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        dx1, dy1 = p[0] - r[0], p[1] - r[1]
        return min(dx**2 + dy**2, dx1**2 + dy1**2) < self.catch_radius2
    

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 100))
        self.chaser.setheading(180)
        self.myturtle.setpos((+init_dist / 2, -100))
        self.myturtle.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec   
        self.timer = time.time()
        self.score = 0
        self.level = 1
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.runner.pos(), self.runner.heading())
        self.chaser.run_ai(self.chaser.pos(), self.chaser.heading())
        self.myturtle.run_ai(self.myturtle.pos(), self.myturtle.heading())

        # TODO) You can do something here and follows.
        #myturtle은 플레이어를 추적함
        if random.randint(0,2) == 0:
            angle = self.myturtle.towards(self.runner.pos())
            self.myturtle.setheading(angle)
            self.myturtle.forward(self.myturtle.step_move)
            
        #거북이가 맵 밖으로 나가지 못하게    
        if self.runner.xcor() > 350:
            self.runner.setpos(350,self.runner.ycor())
        elif self.runner.xcor() < -350:
            self.runner.setpos(-350,self.runner.ycor())
        elif self.runner.ycor() > 350:
            self.runner.setpos(self.runner.xcor(),350)
        elif self.runner.ycor() < -350:
            self.runner.setpos(self.runner.xcor(),-350)
        
        
        is_catched = self.is_catched()
        
        timer = int(time.time()-self.timer)
       
        #시간이 지날수록 난이도 증가
        if timer%5 == 0:
            self.chaser.step_move += 10
            self.chaser.step_turn += 5
            self.myturtle.step_move += 5
            self.level += 1
        
        #난이도가 오르면 점수 증가폭 상승
        self.score = self.score + self.level
        
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'경과 시간 : {timer} 점수 : {self.score}')
        
        if(is_catched):
            tk.messagebox.showinfo("Game Over", f'Score : {self.score}')
        else:
            # Note) The following line should be the last of this function to keep the game playing
            self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=5, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=20):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.left(self.step_turn)
            self.forward(self.step_move)
        elif mode == 1:
            self.right(self.step_turn)            
            self.forward(self.step_move)
        else :
            self.forward(self.step_move)
            
        if(self.xcor() > 350 or self.xcor() < -350 or self.ycor() > 350 or self.ycor() < -350):
            self.right(180)
            self.forward(self.step_move)
            
class ChaseMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=5, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        self.forward(self.step_move)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    chaser = RandomMover(screen)
    runner = ManualMover(screen)
    myturtle = ChaseMover(screen)

    game = RunawayGame(screen, runner, chaser, myturtle)
    game.start()
    screen.mainloop()

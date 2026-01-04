#include <ncurses.h>
#include <vector>
#include <utility>
#include <cstdlib>
#include <ctime>

// ---------------- ENUM ----------------
enum Direction { UP, DOWN, LEFT, RIGHT };

// ---------------- SNAKE CLASS ----------------
class Snake {
private:
    std::vector<std::pair<int,int>> body;
    Direction dir;

public:
    Snake(int startY, int startX) {
        dir = RIGHT;
        body.push_back({startY, startX});
        body.push_back({startY, startX - 1});
        body.push_back({startY, startX - 2});
    }

    void setDirection(Direction newDir) {
        // prevent instant reverse
        if ((dir == UP && newDir == DOWN) ||
            (dir == DOWN && newDir == UP) ||
            (dir == LEFT && newDir == RIGHT) ||
            (dir == RIGHT && newDir == LEFT))
            return;

        dir = newDir;
    }

    void move(bool grow = false) {
        int y = body[0].first;
        int x = body[0].second;

        if (dir == UP) y--;
        if (dir == DOWN) y++;
        if (dir == LEFT) x--;
        if (dir == RIGHT) x++;

        body.insert(body.begin(), {y, x});
        if (!grow)
            body.pop_back();
    }

    void draw() {
        for (auto seg : body)
            mvaddch(seg.first, seg.second, 'O');
    }

    std::pair<int,int> getHead() {
        return body[0];
    }

    bool checkSelfCollision() {
        auto head = body[0];
        for (size_t i = 1; i < body.size(); i++) {
            if (body[i] == head)
                return true;
        }
        return false;
    }
};

// ---------------- FOOD CLASS ----------------
class Food {
private:
    int y, x;

public:
    Food(int maxY, int maxX) {
        respawn(maxY, maxX);
    }

    void respawn(int maxY, int maxX) {
        y = rand() % (maxY - 2) + 1;
        x = rand() % (maxX - 2) + 1;
    }

    void draw() {
        mvaddch(y, x, 'X');
    }

    std::pair<int,int> getPos() {
        return {y, x};
    }
};

// ---------------- MAIN ----------------
int main() {
    srand(time(0));

    initscr();
    noecho();
    curs_set(0);
    keypad(stdscr, TRUE);

    int maxY, maxX;
    getmaxyx(stdscr, maxY, maxX);

    bool playAgain = true;

    while (playAgain) {
        // -------- RESET GAME --------
        nodelay(stdscr, TRUE);

        Snake snake(maxY / 2, maxX / 2);
        Food food(maxY, maxX);

        bool running = true;
        int score = 0;

        // -------- GAME LOOP --------
        while (running) {
            int ch = getch();

            if (ch == 'q') running = false;
            if (ch == KEY_UP)    snake.setDirection(UP);
            if (ch == KEY_DOWN)  snake.setDirection(DOWN);
            if (ch == KEY_LEFT)  snake.setDirection(LEFT);
            if (ch == KEY_RIGHT) snake.setDirection(RIGHT);

            bool grow = false;
            if (snake.getHead() == food.getPos()) {
                score += 10;
                grow = true;
                food.respawn(maxY, maxX);
            }

            snake.move(grow);

            auto head = snake.getHead();

            // wall collision
            if (head.first <= 0 || head.first >= maxY - 1 ||
                head.second <= 0 || head.second >= maxX - 1) {
                running = false;
            }

            // self collision
            if (snake.checkSelfCollision()) {
                running = false;
            }

            clear();
            snake.draw();
            food.draw();
            mvprintw(0, 2, "Score: %d | q: quit", score);
            refresh();

            napms(100);
        }

        // -------- GAME OVER SCREEN --------
        nodelay(stdscr, FALSE);
        clear();
        mvprintw(maxY / 2 - 1, maxX / 2 - 5, "GAME OVER");
        mvprintw(maxY / 2,     maxX / 2 - 10, "Final Score: %d", score);
        mvprintw(maxY / 2 + 2, maxX / 2 - 15, "Press R to Restart");
        mvprintw(maxY / 2 + 3, maxX / 2 - 15, "Press Q to Quit");
        refresh();

        int choice;
        while (true) {
            choice = getch();
            if (choice == 'r' || choice == 'R') {
                playAgain = true;
                break;
            }
            if (choice == 'q' || choice == 'Q') {
                playAgain = false;
                break;
            }
        }
    }

    endwin();
    return 0;
}

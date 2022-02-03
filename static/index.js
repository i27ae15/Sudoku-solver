const line_color = 'black';
let numSolutions = null;
let currentSolution = 1;
let rightArrow = document.getElementById('rightArrow');
let leftArrow = document.getElementById('leftArrow');
let solutions = null;


function creatingGrid(sudokuSize) {
    let squares = document.getElementsByClassName('block');

    for (let n = 0; n < squares.length; n++) {
        currentSquare = squares[n];

        x = parseInt(currentSquare.classList[1]);

        y = parseInt(currentSquare.classList[2][1]);

        boarders = function (size) {
            return `${line_color} solid ${size}px`;
        }

        if (x % 3 == 0) {
            currentSquare.style.borderTop = boarders(2);
        }

        if (currentSquare.classList[1] == `${sudokuSize - 1}`) {
            currentSquare.style.borderBottom = boarders(2);
        }

        if (y % 3 == 0) {
            currentSquare.style.borderLeft = boarders(2);
        }

        if (currentSquare.classList[2] == `y${sudokuSize - 1}`) {
            currentSquare.style.borderRight = boarders(2);
        }

        if (y == 2 || y == 5) {
            currentSquare.style.borderRight = boarders(0);
        }

        if (x == 2 || x == 5) {
            currentSquare.style.borderBottom = boarders(0);
        }
    }
}


function convertInputsToMatrix() {

    let squares = document.getElementsByTagName('input');

    let matrix = [];
    let currentRow = 0;
    let currentIndex = 0;

    while (currentRow < 9) {
        let currentArray = [];

        for (let n = 0; n < 9; n++) {

            currentSquare = squares[currentIndex];
            currentValue = currentSquare.value;

            if (currentValue == '') {
                currentValue = 0;
            } else {
                currentValue = parseInt(currentValue);
            }

            currentArray.push(currentValue);
            currentIndex++;
        }

        currentRow++;
        matrix.push(currentArray);
    }

    return matrix;
}


function validateSudoku(size, sudoku) {

    for (let row = 0; row < sudoku.length; row++) {
        for (let column = 0; column < sudoku.length; column++) {
            if (!validate_row_column(row, column, sudoku, size)) {
                return false;
            }
        }
    }

    return true;
}


function validate_row_column(x, y, matrix, size) {

    let row = [];
    let column = [];

    for (let n = 0; n < size; n++) {
        if (row.includes(matrix[n][y]) || column.includes(matrix[x][n])) {
            return false;
        }

        if (matrix[n][y] != 0) {
            row.push(matrix[n][y]);
        }

        if (matrix[x][n] != 0) {
            column.push(matrix[x][n]);
        }

        // remember to validate also the square
        // thank you andres from the past

        let start_x_square = x - x % 3;
        let start_y_square = y - y % 3;

        let numbersInSquare = [];

        for (let x = 0; x < 3; x++) {
            for (let y = 0; y < 3; y++) {

                if (numbersInSquare.includes(matrix[start_x_square + x][start_y_square + y])) {        
                    return false;
                }
                if (matrix[start_x_square + x][start_y_square + y] != 0) {
                    numbersInSquare.push(matrix[start_x_square + x][start_y_square + y]);
                }
            }
        }

    }


    return true
}


function reset_sudoku() {
    let squares = document.getElementsByTagName('input');
    for (let n = 0; n < squares.length; n++) {
        squares[n].value = '';
    }

    document.getElementById('sudokuChanger').classList.add('invisible');
    rightArrow.classList.add('invisible');
    leftArrow.classList.add('invisible');

}


function putDataIntoGrid(matrix) {

    for (let x = 0; x < matrix.length; x++) {
        for (let y = 0; y < matrix.length; y++) {
            document.getElementById(`x${x}-y${y}`).value = matrix[x][y]
        }
    }

}


document.getElementById('solve').addEventListener('click', function () {
    let matrix = convertInputsToMatrix();

    if (validateSudoku(size = 9, sudoku = matrix)) {
        $.ajax({
            type: 'POST',
            url: "/solve_sudoku",
            data: JSON.stringify({
                "sudoku": matrix,
                "max_solutions": 5
            }),
            contentType: 'application/json; charset=utf-8',
            success: function (data) {

                solutions = data.solutions;
                putDataIntoGrid(solutions[0])

                pMul = document.getElementById('pMultiple');
                sChanger = document.getElementById('sudokuChanger');
                numSolutions = data.num_solutions;

                if (numSolutions > 1) {
                    sChanger.classList.remove('invisible');
                    pMul.textContent = `At least ${numSolutions} solutions found for this sudoku`;
                } else {
                    sChanger.classList.add('invisible');
                }

            }
        });
    } else {
        alert('This is not a valid sudoku');
    }

})


function sudokuChanger(direction) {
    "direction === 0 is for left"
    "direction === 1 is for right"

    if (currentSolution === 1) {
        leftArrow.classList.remove('invisible');
    }

    if (currentSolution === numSolutions) {
        rightArrow.classList.remove('invisible');
    }

    if (direction === 1) {


        if (currentSolution == numSolutions - 1) {
            rightArrow.classList.add('invisible');
        }

        currentSolution++;
        putDataIntoGrid(solutions[currentSolution - 1]);

    } else {

        if (currentSolution == 2) {
            leftArrow.classList.add('invisible');
        }

        currentSolution--;
        putDataIntoGrid(solutions[currentSolution - 1]);

    }
}
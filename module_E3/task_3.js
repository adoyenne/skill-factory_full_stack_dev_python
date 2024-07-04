function createAdder(firstNumber) {
    return function(secondNumber) {
        return firstNumber + secondNumber;
    };
}

// Let's check:
const addTwo = createAdder(2);
console.log(addTwo(10)); 

const addFive = createAdder(5);
console.log(addFive(20));
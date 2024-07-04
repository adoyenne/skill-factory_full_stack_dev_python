function analyzeArray(arr) {
    let evenCount = 0;
    let oddCount = 0;
    let zeroCount = 0;

    arr.forEach(element => {
        if (typeof element === 'number') {
            if (element === 0) {
                zeroCount++;
            } else if (element % 2 === 0) {
                evenCount++;
            } else {
                oddCount++;
            }
        }
    });

    console.log(`Even numbers: ${evenCount}`);
    console.log(`Odd numbers: ${oddCount}`);
    console.log(`Number of zeroes: ${zeroCount}`);
}

// Here is the example:
const testArray = [0, 1, 2, 4, 4, 5, 'world', null, 0, 3, 6, 'hello', 7, 0, undefined];
analyzeArray(testArray);
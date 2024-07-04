function printNumberswithInterval(start, end) {
    let current = start;

    const intervalId = setInterval(() => {
        console.log(current);

        if (current === end) {
            clearInterval(intervalId);
        }

        current++;
    }, 1000); //1000 miliseconds
}

// Testing:
printNumberswithInterval(5, 15);
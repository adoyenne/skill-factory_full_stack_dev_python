function isSimple(num) {
    if (num > 1000) {
        console.log("Incorrect enter, try again!");
        return;
    }

    if (num < 2) {
        console.log(`${num} is not a simple number`);
        return;
    }

    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) {
            console.log(`${num} is not a simple number`);
            return;
        }
    }

    console.log(`${num} is a simple number`);
}

// Let's check:
isSimple(0);
isSimple(1);
isSimple(2);
isSimple(995);
isSimple(1001);
const numbertoPower = (x, n) => {
    let result = 1;
    for (let i = 0; i < n; i++) {
        result *= x;
    }
    return result;
};

// Testing:
console.log(numbertoPower(3, 3));
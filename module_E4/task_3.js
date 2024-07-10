function createObjectWithoutPrototype() {
    return Object.create(null);
}

// let's test it:
const obj = createObjectWithoutPrototype();
console.log(obj);

console.log(Object.getPrototypeOf(obj));
console.log(obj.toString);
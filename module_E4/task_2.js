function hasProperty(propName, obj) {
    return obj.hasOwnProperty(propName);
}


const exampleObject = {
    ownProperty1: 'value1',
    ownProperty2: 'value2'
};

console.log(hasProperty('ownProperty1', exampleObject));
console.log(hasProperty('ownProperty3', exampleObject));
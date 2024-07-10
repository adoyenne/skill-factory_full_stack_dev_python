// Task 1:

function logOwnProperties(obj) {
    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            console.log(key + ': ' + obj[key]);
        }
    }
}

// Testing:
const exampleObject = {
    ownProperty1: 'value1',
    ownProperty2: 'value2'
};

// 
Object.prototype.inheritedProperty = 'inheritedValue';

logOwnProperties(exampleObject);

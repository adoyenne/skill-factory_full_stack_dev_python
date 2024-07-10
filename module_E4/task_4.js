//консольное приложение: электроприборы

// Родительская функция-конструктор для электроприборов
function ElectricalAppliance(name, power) {
    this.name = name;
    this.power = power;
    this.isPluggedIn = false;
}

// Метод для включения эл прибора в розетку
ElectricalAppliance.prototype.plugIn = function() {
    this.isPluggedIn = true;
    console.log(`${this.name} is plugged in.`);
};

// Метод для выключения эл прибора из розетки
ElectricalAppliance.prototype.unplug = function() {
    this.isPluggedIn = false;
    console.log(`${this.name} is unplugged.`);
};

// Создание конкретного эл прибора - настольной лампы
function DeskLamp(power, brightness) {
    ElectricalAppliance.call(this, 'Desk Lamp', power);
    this.brightness = brightness;
}

// Установка делегирующей связи [[Prototype]] для настольной лампы
DeskLamp.prototype = Object.create(ElectricalAppliance.prototype);
DeskLamp.prototype.constructor = DeskLamp;

// Собственный метод настольной лампы
DeskLamp.prototype.adjustBrightness = function(level) {
    this.brightness = level;
    console.log(`${this.name} brightness adjusted to ${this.brightness}.`);
};

// Создание конкретного прибора - компьютера
function Computer(power, brand) {
    ElectricalAppliance.call(this, 'Computer', power);
    this.brand = brand;
}

// Установка делегирующей связи [[Prototype]] для компьютера
Computer.prototype = Object.create(ElectricalAppliance.prototype);
Computer.prototype.constructor = Computer;

// Собственный метод компьютера
Computer.prototype.installSoftware = function(software) {
    console.log(`${this.name} is installing ${software}.`);
};

// Создание экземпляров каждого эл прибора
const myDeskLamp = new DeskLamp(15, 'medium');
const myComputer = new Computer(100, 'Dell');

// Включение эл приборов в розетку
myDeskLamp.plugIn();
myComputer.plugIn();

// Использование собственных методов эл приборов
myDeskLamp.adjustBrightness('high');
myComputer.installSoftware('Photoshop');

// Подсчет общей потребляемой мощности
function calculateTotalPower(appliances) {
    return appliances.reduce((total, appliance) => {
        return total + (appliance.isPluggedIn ? appliance.power : 0);
    }, 0);
}

// Создание массива эл приборов
const appliances = [myDeskLamp, myComputer];

// Подсчет и вывод общей потребляемой мощности
const totalPower = calculateTotalPower(appliances);
console.log(`Total power consumption: ${totalPower}W`);
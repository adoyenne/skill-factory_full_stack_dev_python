//консольное приложение: электроприборы (c использованием классов)


// Родительский класс для электроприборов
class ElectricalAppliance {
    constructor(name, power) {
        this.name = name;
        this.power = power;
        this.isPluggedIn = false;
    }

    // Метод для включения эл прибора в розетку
    plugIn() {
        this.isPluggedIn = true;
        console.log(`${this.name} is plugged in.`);
    }

    // Метод для выключения эл прибора из розетки
    unplug() {
        this.isPluggedIn = false;
        console.log(`${this.name} is unplugged.`);
    }
}

// Класс для настольной лампы
class DeskLamp extends ElectricalAppliance {
    constructor(power, brightness) {
        super('Desk Lamp', power);
        this.brightness = brightness;
    }

    // Метод для настройки яркости настольной лампы
    adjustBrightness(level) {
        this.brightness = level;
        console.log(`${this.name} brightness adjusted to ${this.brightness}.`);
    }
}

// Класс для компьютера
class Computer extends ElectricalAppliance {
    constructor(power, brand) {
        super('Computer', power);
        this.brand = brand;
    }

    // Метод для установки программного обеспечения на компьютер
    installSoftware(software) {
        console.log(`${this.name} is installing ${software}.`);
    }
}

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

// Создание массива приборов
const appliances = [myDeskLamp, myComputer];

// Подсчет и вывод общей потребляемой мощности:
const totalPower = calculateTotalPower(appliances);
console.log(`Total power consumption: ${totalPower}W`);
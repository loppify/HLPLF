function checkValidJSON(jsonString) {
    try {
        JSON.parse(jsonString);
        return "дійсний JSON";
    } catch (error) {
        return "недійсний JSON";
    }
}

const testCases = [
    '{"name": "Ivan", "age": 20}',
    '{name: "Ivan", age: 20}',
    '["apple", "banana"]',
    'Just a string'
];

testCases.forEach((str, index) => {
    console.log(`Тест ${index + 1}: "${str}" -> ${checkValidJSON(str)}`);
});

function getHoffmanCoefficient(months) {
    let sum = 0;
    for (let i = 1; i <= months; i++) {
        sum += 1 / (1 + 0.05 * (i / 12));
    }
    return Math.min(sum, 240);
}

function getGadongMonths(age, type, yearsVal) {
    if (type === 'temporary') {
        return yearsVal * 12;
    }
    let remainingYears = 65 - age;
    if (remainingYears <= 0) {
        if (age >= 62 && age < 67) return 36;
        else if (age >= 67 && age < 76) return 24;
        else return 12;
    }
    return remainingYears * 12;
}

// Inputs
const birthDate = new Date('1992-02-19');
const accidentDate = new Date('2026-02-19');
const age = 34; // 2026 - 1992 = 34
const hospDays = 60;
const ratio = 18;
const MONTHLY_COMMON_WAGE = 3284525;
const baseMonthlyIncome = MONTHLY_COMMON_WAGE;

const months = getGadongMonths(age, 'permanent');
const hospMonths = Math.round(hospDays / 30);

const hospH = getHoffmanCoefficient(hospMonths);
const lossHosp = Math.round(baseMonthlyIncome * 1.0 * hospH);

let lossRemaining = 0;
let remainingH = 0;
if (months > hospMonths) {
    remainingH = getHoffmanCoefficient(months) - hospH;
    lossRemaining = Math.round(baseMonthlyIncome * (ratio / 100) * remainingH);
}

const totalLossOfEarnings = lossHosp + lossRemaining;

console.log(`Age: ${age}`);
console.log(`Total Gadong Months: ${months}`);
console.log(`Hosp Months: ${hospMonths}`);
console.log(`Hosp Hoffman H: ${hospH.toFixed(4)}`);
console.log(`Remaining Hoffman H: ${remainingH.toFixed(4)}`);
console.log(`Loss during Hosp (100%): ${lossHosp.toLocaleString('ko-KR')}원`);
console.log(`Loss after Hosp (18%): ${lossRemaining.toLocaleString('ko-KR')}원`);
console.log(`Total Loss of Earnings: ${totalLossOfEarnings.toLocaleString('ko-KR')}원`);

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const VAULT_PATH = 'C:\\Users\\SB\\Documents\\손사봇볼트\\20_Precedents';
const DATA_FILE_PATH = path.join(__dirname, 'precedent_court_data.js');

function parseMarkdown(content) {
    const data = {
        title: "",
        case_no: "",
        court: "",
        year: "",
        date: "",
        case_type: "",
        core_issue: "",
        acceptance_criteria: [],
        rejection_criteria: [],
        fact_summary: [],
        court_decision: [],
        practical_points: [],
        expected_rebuttals: [],
        counter_logic: [],
        keywords: []
    };

    // Extract frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
        const fm = frontmatterMatch[1];
        const titleMatch = fm.match(/^title:\s*"?(.*?)"?$/m);
        if (titleMatch) data.title = titleMatch[1].trim();

        const tagsMatch = fm.match(/^tags:\s*\n((?:\s*-\s*".*?"\s*\n?)*)/m);
        if (tagsMatch) {
            data.keywords = tagsMatch[1].split('\n')
                .map(t => t.replace(/^\s*-\s*"/, '').replace(/"\s*$/, '').trim())
                .filter(t => t);
        }
    }

    // Fallback for title if not in frontmatter
    if (!data.title) {
        const h1Match = content.match(/^#\s+(.+)$/m);
        if (h1Match) data.title = h1Match[1].trim();
    }

    // Regex to extract content between ## headings
    const extractSection = (heading) => {
        const regex = new RegExp(`^##\\s+${heading}\\s*\\n([\\s\\S]*?)(?=\\n## |$)`, 'm');
        const match = content.match(regex);
        return match ? match[1].trim() : '';
    };

    const parseList = (text) => {
        return text.split('\n')
            .map(line => line.replace(/^-\s*/, '').replace(/^\*\*.*?\*\*:\s*/, '').trim())
            .filter(line => line.length > 0);
    };

    // Parse '기본 정보'
    const basicInfo = extractSection('기본 정보');
    if (basicInfo) {
        const noMatch = basicInfo.match(/사건번호:\s*(.+)/);
        if (noMatch) data.case_no = noMatch[1].trim();

        const courtMatch = basicInfo.match(/법원:\s*(.+)/);
        if (courtMatch) data.court = courtMatch[1].trim();

        const yearMatch = basicInfo.match(/선고연도:\s*(.+)/);
        if (yearMatch) data.year = yearMatch[1].trim();

        const dateMatch = basicInfo.match(/선고일:\s*(.+)/);
        if (dateMatch) data.date = dateMatch[1].trim();

        const typeMatch = basicInfo.match(/사건유형:\s*(.+)/);
        if (typeMatch) data.case_type = typeMatch[1].trim();
    }

    // Parse other sections
    const coreIssueText = extractSection('핵심 쟁점');
    data.core_issue = parseList(coreIssueText).join(' '); // usually 1 line

    data.acceptance_criteria = parseList(extractSection('인정 요건'));
    data.rejection_criteria = parseList(extractSection('배척 요건 또는 한계'));
    data.fact_summary = parseList(extractSection('사실관계 요약'));
    data.court_decision = parseList(extractSection('법원의 판단'));
    data.practical_points = parseList(extractSection('실무 적용 포인트'));
    data.expected_rebuttals = parseList(extractSection('보험사 예상 반론'));
    data.counter_logic = parseList(extractSection('반박 논리'));

    return data;
}

function syncObsidian() {
    console.log('Starting sync...');
    if (!fs.existsSync(VAULT_PATH)) {
        throw new Error(`Vault path not found: ${VAULT_PATH}`);
    }

    const files = fs.readdirSync(VAULT_PATH).filter(f => f.endsWith('.md'));
    const precedents = [];

    for (const file of files) {
        const filePath = path.join(VAULT_PATH, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const data = parseMarkdown(content);
        if (data.title) {
            precedents.push(data);
        }
    }

    const jsContent = `const court_precedents = ${JSON.stringify(precedents, null, 4)};\n`;
    fs.writeFileSync(DATA_FILE_PATH, jsContent, 'utf8');
    console.log(`Updated ${DATA_FILE_PATH} with ${precedents.length} precedents.`);

    try {
        console.log('Committing to GitHub...');
        execSync('git add precedent_court_data.js', { cwd: __dirname });
        
        const status = execSync('git status --porcelain', { cwd: __dirname }).toString();
        if (status.includes('precedent_court_data.js')) {
            execSync('git commit -m "feat: 옵시디언 동기화 (손사봇볼트 판례 데이터 업데이트)"', { cwd: __dirname });
            console.log('Pushing to GitHub...');
            execSync('git push origin main', { cwd: __dirname });
            console.log('Sync and push successful!');
        } else {
            console.log('No changes detected in precedent_court_data.js.');
        }
        return { success: true, count: precedents.length, changed: status.includes('precedent_court_data.js') };
    } catch (e) {
        console.error('Git execution failed:', e.message);
        throw e;
    }
}

if (require.main === module) {
    syncObsidian();
}

module.exports = { syncObsidian };

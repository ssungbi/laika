const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');

const VAULT_PATH = 'C:\\Users\\SB\\Documents\\손사봇볼트\\20_Precedents';
const DATA_FILE_PATH = path.join(__dirname, 'precedent_court_data.js');

// R2 Configuration
const BUCKET_NAME = 'laika-document';
const UPLOAD_DIR = 'C:\\Users\\SB\\Desktop\\R2_Upload';
const PDF_SOURCE_DIR = '\\\\wsl$\\Ubuntu-24.04\\home\\sb\\.openclaw\\workspace\\sonsabot\\손해사정\\판례라이브러리\\원본';
const R2_BASE_URL = 'https://pub-7fb437306e7041f3adecc45dd8eae262.r2.dev';

const s3Client = new S3Client({
    region: 'auto',
    endpoint: 'https://695861ff3b657e380590aade97387ac0.r2.cloudflarestorage.com',
    credentials: {
        accessKeyId: 'a3cc89f4c41bc676ae3af230ce932c98',
        secretAccessKey: 'ac2fb4548dfb6d63b87f4ed8a9e6e3ce992f8bbea1e5446b028f06b8f4b4e057',
    },
});

async function processAndUploadPdfs() {
    console.log('Checking for new PDFs to process and upload...');
    if (!fs.existsSync(UPLOAD_DIR)) {
        fs.mkdirSync(UPLOAD_DIR);
    }
    if (!fs.existsSync(PDF_SOURCE_DIR)) {
        console.log(`Original PDF directory not found: ${PDF_SOURCE_DIR}`);
        return;
    }

    const originalPdfs = fs.readdirSync(PDF_SOURCE_DIR).filter(f => f.endsWith('.pdf'));
    const mdFiles = fs.readdirSync(VAULT_PATH).filter(f => f.endsWith('.md'));
    let newUploadsCount = 0;

    for (const pdf of originalPdfs) {
        const caseMatch = pdf.match(/20[0-9]{2}[가-힣]+[0-9]+/);
        if (!caseMatch) continue;
        
        const caseNo = caseMatch[0];
        const newFileName = `${caseNo}.pdf`;
        const targetPdfPath = path.join(UPLOAD_DIR, newFileName);
        
        // If it's already in R2_Upload, we assume it's uploaded and skipped to save API calls
        if (fs.existsSync(targetPdfPath)) continue;
        
        // It's a new PDF!
        console.log(`Found new PDF: ${pdf} -> ${newFileName}`);
        fs.copyFileSync(path.join(PDF_SOURCE_DIR, pdf), targetPdfPath);
        
        // Upload to R2
        try {
            console.log(`Uploading ${newFileName} to R2...`);
            const fileStream = fs.createReadStream(targetPdfPath);
            await s3Client.send(new PutObjectCommand({
                Bucket: BUCKET_NAME,
                Key: newFileName,
                Body: fileStream,
                ContentType: 'application/pdf'
            }));
            console.log(`✅ Uploaded: ${newFileName}`);
            newUploadsCount++;
        } catch (err) {
            console.error(`❌ Upload failed for ${newFileName}`, err.message);
            continue; // Skip markdown update if upload fails
        }
        
        // Update matching Markdown file
        const targetMdFile = mdFiles.find(md => md.startsWith(caseNo + '_') || md === `${caseNo}.md`);
        if (targetMdFile) {
            const mdPath = path.join(VAULT_PATH, targetMdFile);
            let content = fs.readFileSync(mdPath, 'utf8');
            const pdfUrlLine = `pdf_url: "${R2_BASE_URL}/${newFileName}"`;
            if (!content.includes('pdf_url:')) {
                if (content.startsWith('---')) {
                    content = content.replace(/^---\r?\n/, `---\n${pdfUrlLine}\n`);
                } else {
                    content = `---\n${pdfUrlLine}\n---\n\n` + content;
                }
                fs.writeFileSync(mdPath, content, 'utf8');
                console.log(`Updated MD: ${targetMdFile}`);
            }
        }
    }
    
    if (newUploadsCount === 0) {
        console.log('No new PDFs to process.');
    } else {
        console.log(`Successfully processed and uploaded ${newUploadsCount} new PDFs.`);
    }
}

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
        keywords: [],
        consumer_result: "",
        pdf_url: ""
    };

    // Extract frontmatter
    const frontmatterMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
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

        const pdfUrlMatch = fm.match(/^pdf_url:\s*"?(.*?)"?$/m);
        if (pdfUrlMatch) {
            data.pdf_url = pdfUrlMatch[1].trim();
        }
    }

    // Fallback for title if not in frontmatter
    if (!data.title) {
        const h1Match = content.match(/^#\s+(.+)$/m);
        if (h1Match) data.title = h1Match[1].trim();
    }

    // Regex to extract content between ## headings
    const extractSection = (heading) => {
        const regex = new RegExp(`(?:^|\\n)##\\s+${heading}\\s*\\n([\\s\\S]*?)(?=\\n## |$)`);
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
    if (data.title && data.title.includes('2003나84240')) {
        console.log("basicInfo extracted:", basicInfo);
    }
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

        const resultMatch = basicInfo.match(/소비자 유불리.*?:\s*(.+)/);
        if (resultMatch) {
            let res = resultMatch[1].trim();
            // Remove markdown bold if present
            res = res.replace(/^\*\*|\*\*$/g, '');
            data.consumer_result = res;
        }
    }

    // Parse other sections
    const coreIssueText = extractSection('핵심 쟁점');
    if (coreIssueText) {
        const lines = coreIssueText.split('\n');
        let formattedLines = [];
        let sectionCount = 1;
        let skipSection = false;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line.startsWith('- **') && line.includes('**:')) {
                const match = line.match(/\*\*(.*?)\*\*(?:.*?):\s*(.*)/);
                if (match) {
                    const headerText = match[1].trim();
                    if (headerText.includes('실무 확장 쟁점')) {
                        skipSection = true;
                        continue;
                    }
                    skipSection = false;
                    
                    const contentText = match[2].trim();
                    if (contentText) {
                        formattedLines.push(`${sectionCount}) ${headerText} : ${contentText}`);
                    } else {
                        formattedLines.push(`${sectionCount}) ${headerText} :`);
                    }
                    sectionCount++;
                }
            } else if (!skipSection) {
                if (line.startsWith('-')) {
                    const contentText = line.replace(/^- /, '').trim();
                    formattedLines.push(`  - ${contentText}`);
                } else if (line.length > 0) {
                    formattedLines.push(`  ${line}`);
                }
            }
        }
        data.core_issue = formattedLines.join('\n').trim();
    } else {
        data.core_issue = '';
    }

    data.acceptance_criteria = parseList(extractSection('인정 요건'));
    data.rejection_criteria = parseList(extractSection('배척 요건 또는 한계'));
    data.fact_summary = parseList(extractSection('사실관계 요약'));
    data.court_decision = parseList(extractSection('법원의 판단'));
    data.practical_points = parseList(extractSection('실무 적용 포인트'));
    data.expected_rebuttals = parseList(extractSection('보험사 예상 반론'));
    data.counter_logic = parseList(extractSection('반박 논리'));

    return data;
}

async function syncObsidian() {
    console.log('Starting sync pipeline...');
    
    try {
        await processAndUploadPdfs();
    } catch (err) {
        console.error('Error during PDF upload phase:', err);
        // Continue with markdown parsing even if PDF upload fails
    }

    if (!fs.existsSync(VAULT_PATH)) {
        throw new Error(`Vault path not found: ${VAULT_PATH}`);
    }

    const files = fs.readdirSync(VAULT_PATH).filter(f => f.endsWith('.md'));
    const mdPrecedents = [];
    const mdCaseNos = new Set();

    for (const file of files) {
        const filePath = path.join(VAULT_PATH, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const data = parseMarkdown(content);
        if (data.title) {
            mdPrecedents.push(data);
            if (data.case_no) mdCaseNos.add(data.case_no);
        }
    }

    // 기존 데이터 읽기 및 병합 (마크다운 없이 다른 봇이 직접 JS에 넣은 데이터 보존)
    let existingData = [];
    try {
        if (fs.existsSync(DATA_FILE_PATH)) {
            const existingContent = fs.readFileSync(DATA_FILE_PATH, 'utf8');
            const existingDataStr = existingContent.replace('const court_precedents = ', '').trim().replace(/;$/, '');
            existingData = JSON.parse(existingDataStr);
        }
    } catch (e) {
        console.error('기존 데이터를 파싱하는데 실패했습니다:', e);
    }

    // 마크다운 폴더에 없는 사건번호만 기존 데이터에서 살리기
    const preservedPrecedents = existingData.filter(d => d.case_no && !mdCaseNos.has(d.case_no));
    
    // 최종 병합
    const finalPrecedents = [...mdPrecedents, ...preservedPrecedents];

    const jsContent = `const court_precedents = ${JSON.stringify(finalPrecedents, null, 4)};\n`;
    fs.writeFileSync(DATA_FILE_PATH, jsContent, 'utf8');
    console.log(`Updated ${DATA_FILE_PATH} with ${finalPrecedents.length} precedents (Parsed: ${mdPrecedents.length}, Preserved: ${preservedPrecedents.length}).`);

    try {
        console.log('Committing to GitHub...');
        execSync('git add precedent_court_data.js', { cwd: __dirname });
        
        const status = execSync('git status --porcelain', { cwd: __dirname }).toString();
        if (status.includes('precedent_court_data.js')) {
            execSync('git commit -m "feat: 옵시디언 동기화 (손사봇볼트 판례 데이터 업데이트)"', { cwd: __dirname });
            console.log('Pulling latest from GitHub...');
            execSync('git pull --rebase origin main', { cwd: __dirname });
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
    syncObsidian().then(res => console.log('Finished:', res)).catch(err => console.error(err));
}

module.exports = { syncObsidian };

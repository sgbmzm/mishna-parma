# דבר ראשון עשיתי בוורד חיפוש ^n והחלפה ב: ^n[מעבר טור]
#ואחר כך חיפוש ^m והחלפה ב: ^m[מעבר עמוד]
# ואחר כך חיפוש [מעבר טור] והחלפה ב: [מעבר טור] עם עיצוב גופן: מוסתר
# ואחר כך חיפוש [מעבר טור] והחלפה ב: [מעבר עמוד] עם עיצוב גופן: מוסתר


# דבר ראשון ממירים מקובץ וורד לקובץ HTML כך
### pandoc parma.docx -o file.html --wrap=none

start_text = """

<!DOCTYPE html>
<html lang="he">
<head>
    <meta charset="UTF-8">
    <title>טקסט עברי</title>
    <style>
        /* ===== בסיס לדף ===== */
        body {
            direction: rtl;              /* תצוגה מימין לשמאל */
            text-align: right;           /* מסדר את הטקסט לימין */
            font-size: 1.8rem;
            line-height: 1.4;
            font-family: "Noto Sans Hebrew", "Frank Ruehl", "David", sans-serif;
            margin: 0 auto;
            padding: 10rem;
            box-sizing: border-box;
        }

        html, body {
            max-width: 4000px;           /* מאפשר מספיק רוחב לטורים */
            overflow-x: auto;            /* מונע חיתוך אם הדף רחב מדי */
        }

        /* מונע שהאלמנטים הפנימיים ידחפו את הדף לרוחב */
        p, span, strong, sup {
            max-width: 100%;
            overflow-wrap: break-word;
            word-break: break-word;
        }

        /* ===== מבנה עמודים ===== */
        .page {
            display: flex;
            gap: 80px;                   /* מרווח בין טורים */
            width: max-content;           /* העמוד יתפוס רוחב לפי תוכן הטורים */
            margin: 40px auto;
            padding: 60px;
            background: white;
            box-sizing: border-box;
        }

        /* ===== עמודות ===== */
        .column {
            width: 700px;               /* רוחב קבוע לכל טור */
            text-align: justify;          /* מיישר שורות לשני הצדדים */
            text-justify: inter-word;     
            text-align-last: justify;     /* מיישר גם שורה אחרונה */
        }

        /* ===== פתרון ל־justify בכל שורה ===== */
        
        .column p:not(:has(strong))::after {
            content: "";
            display: inline-block;
            width: 100%;
        }
            

        .column p{
            margin: 0;             /* בלי רווח לפני ואחרי כותרת */
        }
        
        .column p:has(strong span[dir="rtl"]) {
            text-align: center;
            text-align-last: center;
        }
        
        .page {
            outline: 1px solid black;
        }
        
        
        .page {
            position: relative;
            outline: 1px solid black; /* אם רוצים מסגרת סביב העמוד */
            margin-bottom: 100px; /* אם רוצים רווח בין מסגרת למסגרת */
        }

        /* מספר דף אוטומטי */
        .page-number {
            position: absolute;
            bottom: 10px;       /* מרחק מהתחתית */
            left: 50%;          /* מרכז */
            transform: translateX(-50%);
            font-size: 1.5rem;
            color: red;
        }

        
        .page {
            position: relative;
        }
        
        
        /* מסתיר את כל ההערות מהתחתית */
        hr + ol {
            display: none;
        }
            
    
    </style>




</head>
<body>



"""



end_text = """

<script>


// עושה שמספור ההערות יהיה לכל עמוד מחדש ולא כברירת מחדל שהמספור רציץ מהתחלה ועד הסוף
// זה חשוב מאוד כי מספור רציף הוא ארוך ומזיז את הטקסט וגם לא תואם למהדורה המודפסת
document.querySelectorAll('.page').forEach(page => {
    let footnotes = page.querySelectorAll('.footnote-ref');
    footnotes.forEach((ref, index) => {
        const sup = ref.querySelector('sup');
        if(sup) sup.textContent = index + 1;  // מספר מחדש מה-1 בכל עמוד
    });
});




// פונקציה ליצירת tooltip חכם
function createSmartTooltip(ref, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'footnote-tooltip';
    tooltip.textContent = text;
    
    Object.assign(tooltip.style, {
        position: 'absolute',
        backgroundColor: '#fff9c4',
        border: '1px solid #ccc',
        padding: '0.5rem',
        borderRadius: '5px',
        boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
        textAlign: 'right', // עברית
        zIndex: '1000',
        display: 'none',
        maxWidth: '300px',
        wordWrap: 'break-word',
        fontSize: '1rem'   // כאן משנה את הגודל
    });

    document.body.appendChild(tooltip);

    function positionTooltip() {
        const rect = ref.getBoundingClientRect();
        const scrollX = window.scrollX || window.pageXOffset;
        const scrollY = window.scrollY || window.pageYOffset;
        tooltip.style.display = 'block';
        tooltip.style.maxWidth = '300px';
        
        // בודק אם יש מקום מימין או שמאל
        if (rect.right + tooltip.offsetWidth + 10 > window.innerWidth) {
            // אין מקום מימין → מייצר משמאל
            tooltip.style.left = scrollX + rect.left - tooltip.offsetWidth + 'px';
        } else {
            // מימין
            tooltip.style.left = scrollX + rect.right + 5 + 'px';
        }
        tooltip.style.top = scrollY + rect.top + 'px';
    }

    ref.addEventListener('mouseover', positionTooltip);
    ref.addEventListener('mouseout', () => {
        tooltip.style.display = 'none';
    });
    // גם אם זזים עם העכבר תוך כדי hover
    ref.addEventListener('mousemove', positionTooltip);
}

// מחבר את כל ההערות הקיימות
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.footnote-ref').forEach(ref => {
        const fnId = ref.getAttribute('href').substring(1); // מקבל את id של ההערה
        const fnTextEl = document.getElementById(fnId);
        if (fnTextEl) {
            const text = fnTextEl.innerText.trim();
            createSmartTooltip(ref, text);
        }
    });
});
</script>




<script>
const SYMBOLS = ['*','^','»','˚','$','#', '&'];
const SPECIAL_SYMBOL = '•'; // סימן “חשוב במיוחד”

const originalTextMap = new WeakMap();

function startsWithSymbol(node) {
    return node.nodeType === Node.TEXT_NODE && (SYMBOLS.concat([SPECIAL_SYMBOL]).some(sym => node.textContent.trim().startsWith(sym)));
}

function getSymbolData(ref) {
    let data = { supElements: [], textNodes: [] };
    let el = ref.nextElementSibling;

    while (el) {
        if (el.classList.contains('footnote-ref') || el.tagName === 'OL' || el.tagName === 'ASIDE') break;

        if (el.tagName === 'SUP' && SYMBOLS.concat([SPECIAL_SYMBOL]).some(sym => el.textContent.includes(sym))) {
            data.supElements.push(el);
        }

        if (['SPAN','STRONG','MARK'].includes(el.tagName)) {
            el.querySelectorAll('sup').forEach(sup => {
                if (SYMBOLS.concat([SPECIAL_SYMBOL]).some(sym => sup.textContent.includes(sym))) {
                    data.supElements.push(sup);
                }
            });
            el.childNodes.forEach(node => {
                if (startsWithSymbol(node)) {
                    data.textNodes.push(node);
                    if (!originalTextMap.has(node)) {
                        originalTextMap.set(node, node.textContent);
                    }
                }
            });
        }

        el = el.nextElementSibling;
    }
    return data;
}

function hideSymbols(data) {
    data.supElements.forEach(el => el.style.display = 'none');
    data.textNodes.forEach(node => {
        let text = originalTextMap.get(node) || node.textContent;
        node.textContent = text.replace(new RegExp("^[" + SYMBOLS.join("") + SPECIAL_SYMBOL + "]+"), '');
    });
}

function showSymbols(data) {
    data.supElements.forEach(el => el.style.display = 'inline');
    data.textNodes.forEach(node => {
        node.textContent = originalTextMap.get(node) || node.textContent;
    });
}

function showNone() {
    document.querySelectorAll('.footnote-ref').forEach(ref => {
        ref.style.display = 'none';
        hideSymbols(getSymbolData(ref));
    });
    document.querySelectorAll('aside.footnotes').forEach(el => el.style.display = 'none');
}

function showAll() {
    document.querySelectorAll('.footnote-ref').forEach(ref => {
        ref.style.display = 'inline';
        showSymbols(getSymbolData(ref));
    });
    document.querySelectorAll('aside.footnotes').forEach(el => el.style.display = 'block');
}

function filterBySymbol(symbol) {
    document.querySelectorAll('.footnote-ref').forEach(ref => {
        let data = getSymbolData(ref);
        let hasSymbol = data.supElements.concat(data.textNodes).some(el => el.textContent.includes(symbol));
        
        if (hasSymbol) {
            ref.style.display = 'inline';
            showSymbols(data);
        } else {
            ref.style.display = 'none';
            hideSymbols(data);
        }
    });
    document.querySelectorAll('aside.footnotes').forEach(el => el.style.display = 'block');
}

document.addEventListener('DOMContentLoaded', () => {
    const controls = document.createElement('div');
    controls.id = 'symbol-controls';
    controls.style.position = 'fixed';
    controls.style.top = '20%';
    controls.style.right = '0';
    controls.style.transform = 'translateY(-50%)';
    controls.style.backgroundColor = 'rgba(255,255,255,0.9)';
    controls.style.border = '1px solid #ccc';
    controls.style.padding = '5px';
    controls.style.zIndex = '9999';
    controls.style.transition = 'width 0.3s';
    controls.style.width = '30px'; // רוחב קטן בהתחלה
    controls.style.overflow = 'hidden';
    controls.style.whiteSpace = 'nowrap';
    controls.style.cursor = 'pointer';
    controls.style.boxShadow = '0 0 5px rgba(0,0,0,0.3)';
    
    // תוכן הכפתורים
    controls.innerHTML = `
        <div style="display:flex; flex-direction:column;">
            <button onclick="showAll()">הצג הכל</button>
            <button onclick="showNone()">הסתר הכל</button>
            ${SYMBOLS.map(sym => `<button onclick="filterBySymbol('${sym}')">${sym}</button>`).join('')}
            <button onclick="filterBySymbol('${SPECIAL_SYMBOL}')">${SPECIAL_SYMBOL} (חשוב)</button>
        </div>
    `;

    // הרחבה כשמרחפים מעל
    controls.addEventListener('mouseenter', () => {
        controls.style.width = '200px';
    });
    controls.addEventListener('mouseleave', () => {
        controls.style.width = '30px';
    });

    document.body.appendChild(controls);
});
</script>



<script>
// ב־DOMContentLoaded מוסיפים לכל page את מספר הדף
document.addEventListener("DOMContentLoaded", function() {
    const pages = document.querySelectorAll(".page");
    pages.forEach((page, index) => {
        const pageNumber = document.createElement("div");
        pageNumber.className = "page-number";
        pageNumber.textContent = "עמוד " + (index + 1);
        page.appendChild(pageNumber);
    });
});
</script>





</body>
</html>




"""


def ttt(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:
        html = f.read()
        
    
    html = html.replace("[מעבר טור]<br />","\n\n</div><div class=\"column\">")
    html = html.replace("[מעבר טור]","\n\n</div><div class=\"column\">")
    
    html = html.replace("[מעבר עמוד]<br />\n</span></p>","\n\n</span></p></div></div><div class=\"page\"><div class=\"column\">")
    html = html.replace("[מעבר עמוד]<br />","\n\n</div></div><div class=\"page\"><div class=\"column\">")
    html = html.replace("[מעבר עמוד]","\n\n</div></div><div class=\"page\"><div class=\"column\">")

    # הוספה בתחילת הקובץ ובסופו
    html = start_text + html + end_text

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print("בוצע")
    
    
input_file = "file.html"
output_file = "output.html"
ttt(input_file, output_file)



########### חייבים גם ידנית להוסיף לפני השורה הראשונה של טקסט המשנה את השורה הזו:
#    </span></p></div></div><div class="page"><div class="column">
# וגם צריך לוסיף:
# </div></div>
# לפני השורה של
#<hr />
#<ol>
# שנמצא לפני ההערות

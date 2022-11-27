function onOpenCvReady() {
    let scripts = document.getElementById('calculate_histogram');
    let image_id = scripts.getAttribute('image_id');
    cv['onRuntimeInitialized']=()=>{
        calculate_histogram('imageSrc', 'displayCol')
    };
}

function calculate_histogram(image_id, displayCol) {
    let imgElement = document.getElementById(image_id);
    let canvasOutId = document.getElementById(displayCol).getElementsByTagName('canvas')[0];
    let src = cv.imread(imgElement);
    cv.cvtColor(src, src, cv.COLOR_RGBA2GRAY, 0);
    let srcVec = new cv.MatVector();
    srcVec.push_back(src);
    let accumulate = false;
    let channels = [0];
    let histSize = [256];
    let ranges = [0, 255];
    let hist = new cv.Mat();
    let mask = new cv.Mat();
    let color = new cv.Scalar(255, 255, 255);
    let scale = 2;
    cv.calcHist(srcVec, channels, mask, hist, histSize, ranges, accumulate);
    let result = cv.minMaxLoc(hist, mask);
    let max = result.maxVal;
    let dst = new cv.Mat.zeros(src.rows, histSize[0] * scale,
                               cv.CV_8UC3);
    // draw histogram
    for (let i = 0; i < histSize[0]; i++) {
        let binVal = hist.data32F[i] * src.rows / max;
        let point1 = new cv.Point(i * scale, src.rows - 1);
        let point2 = new cv.Point((i + 1) * scale - 1, src.rows - binVal);
        cv.rectangle(dst, point1, point2, color, cv.FILLED);
    }
    cv.imshow(canvasOutId, dst);//prints in the output canvas
    src.delete(); dst.delete(); srcVec.delete(); mask.delete(); hist.delete();
    displayHistogram(displayCol);
}

/**Displays the output canvas after disabling the loading spinner**/
function displayHistogram(displayCol){
    let spinner = document.getElementById(displayCol).getElementsByTagName('div')[0];
    let canvasOut = spinner.nextElementSibling;

    spinner.classList.add('d-none');
    canvasOut.classList.remove('d-none');
}
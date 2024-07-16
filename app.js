const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = 3000;

// Set storage engine for multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'C:\\Users\\mannu\\XRayCaptioningProject\\public\\')
    },
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});
const upload = multer({ storage: storage });

// Set static folder
app.use(express.static(path.join(__dirname, 'public')));

// Set view engine
app.set('view engine', 'ejs');

// Render index page
app.get('/', (req, res) => {
    res.render('index');
});

// Upload image and generate caption
app.post('/upload', upload.fields([{ name: 'image1', maxCount: 1 }]), (req, res) => {
    // Get uploaded file paths
    const image1Path = req.files['image1'][0].path;
    console.log("Hello");
    // console.log(image1Path, image1Path);
    // Run Python script with uploaded file paths as input
    exec(`py finalScript.py ${image1Path}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        const captions = JSON.parse(stdout.trim()).captions;
        res.json({ result: captions, path: image1Path });
    });
});

app.post('/', (req, res) => {
    // Array of paths
    console.log("Hello123");
    var paths = [
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713257462038.png",
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713257760595.png",
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713258983798.png",
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713259838683.png",
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713260002429.png",
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713264360872.png",
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713264546023.png",
        "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713703567927.png",
        // "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713703631741.png",
        // "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713703809150.png",
        // "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713703819011.png",
        // "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713704008214.png",
        // "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713704533205.png",
        // "C:\\Users\\mannu\\XRayCaptioningProject\\public\\image1-1713704541676.png"
    ];
    const pathsString = paths.join(' ');

    exec(`py finalScript.py ${pathsString}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        const captions = JSON.parse(stdout.trim()).captions;
        console.log(captions);
        res.json({ result: captions });
    });
})

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

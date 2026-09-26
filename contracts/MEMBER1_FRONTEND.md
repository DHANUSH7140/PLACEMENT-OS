# Integration Contract for Member 1 (Lovable Frontend + Firebase)
**Owner:** Member 3 (Data Architecture & Question Intelligence)  
**Target:** Member 1 (Lovable Frontend / React / Firebase Client)

---

## 1. Firebase Client Configuration

Ensure Firebase JS SDK initializes with standard project configuration. The security rules in `firestore.rules` and `storage.rules` are configured to enforce authorization automatically.

```typescript
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  projectId: "placement-os-hackathon",
  storageBucket: "placement-os-documents.appspot.com",
  // ...other standard keys from Member 4 / Firebase console
};

export const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const storage = getStorage(app);
export const auth = getAuth(app);
```

---

## 2. Key Frontend Queries & Constraints

### 2.1. Browsing the Master Question Bank
Students can filter questions by category, difficulty, or target company:

```typescript
import { collection, query, where, orderBy, limit, getDocs } from 'firebase/firestore';

// Query DSA Medium questions ordered by observed frequency
const q = query(
  collection(db, "questions"),
  where("category", "==", "DSA"),
  where("difficulty", "==", "Medium"),
  orderBy("observed_frequency", "desc"),
  limit(20)
);

// Query questions asked by Amazon
const amazonQuery = query(
  collection(db, "questions"),
  where("companies", "array-contains", "Amazon"),
  orderBy("difficulty", "asc"),
  orderBy("observed_frequency", "desc"),
  limit(20)
);
```

> [!IMPORTANT]
> **Dashboard Display Copy:**
> Always render question prevalence as **"Observed Frequency: X"** or **"Seen across Y monitored sources"**.  
> **NEVER** claim "This question has a 95% market frequency" or "Official company leak".

### 2.2. Listening to Student Attempts & Mistakes
Use real-time snapshots so the UI updates immediately when Member 2's evaluation engine finishes grading:

```typescript
import { collection, query, where, orderBy, onSnapshot } from 'firebase/firestore';

const attemptsQuery = query(
  collection(db, "question_attempts"),
  where("student_id", "==", auth.currentUser.uid),
  orderBy("attempted_at", "desc"),
  limit(15)
);

const unsubscribe = onSnapshot(attemptsQuery, (snapshot) => {
  const attempts = snapshot.docs.map(doc => doc.data());
  // Update state in Lovable UI
});
```

---

## 3. Direct Browser-to-Cloud Storage Uploads

Do **NOT** upload heavy files through FastAPI. Use the direct GCS upload flow:

1. **Option A (Firebase Client SDK):**
   ```typescript
   import { ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage';

   const storagePath = `users/${auth.currentUser.uid}/resumes/${Date.now()}_${file.name}`;
   const storageRef = ref(storage, storagePath);
   await uploadBytesResumable(storageRef, file);
   const downloadUrl = await getDownloadURL(storageRef);

   // Then write metadata record to Firestore 'documents' collection:
   await addDoc(collection(db, "documents"), {
     student_id: auth.currentUser.uid,
     document_type: "resume",
     file_name: file.name,
     mime_type: file.type,
     file_size_bytes: file.size,
     gcs_bucket: "placement-os-documents.appspot.com",
     gcs_blob_path: storagePath,
     gcs_public_url: downloadUrl,
     parsing_status: "UPLOADED",
     created_at: new Date().toISOString()
   });
   ```

2. **Option B (FastAPI Pre-signed URL):**  
   Call Member 2's `GET /api/v1/storage/upload-url?doc_type=resume&filename=resume.pdf` to receive a pre-signed PUT URL, then perform a direct HTTP `PUT` from the browser.

---

## 4. Supported Taxonomies for Dropdowns & Filters

The UI dropdowns should populate from these 26 canonical categories:
- `DSA`, `Programming`, `SQL`, `DBMS`, `OS`, `Computer Networks`, `OOP`, `Aptitude`
- `AI`, `ML`, `DL`, `NLP`, `Computer Vision`, `Generative AI`
- `Cloud`, `DevOps`, `Data Analytics`, `Power BI`, `Excel`
- `Web Development`, `System Design`
- `HR`, `Behavioral`, `Communication`, `Project`, `Resume`

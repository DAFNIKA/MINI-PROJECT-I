# database/seed_data.py
"""
Seed data for the SQLite Database.
Contains predefined interview questions, categories, difficulty levels, and detailed ideal answers.
"""

QUESTIONS = [
    # --- TECHNICAL: PYTHON ---
    {
        "question_text": "What is the difference between list and tuple in Python?",
        "ideal_answer": "Lists are mutable, meaning their elements can be modified after creation, and they are defined using square brackets []. Tuples are immutable, meaning they cannot be modified after creation, and they are defined using parentheses (). Lists have a larger memory overhead than tuples, which are more memory-efficient and faster to iterate over. Tuples can be used as keys in dictionaries if they contain immutable elements, whereas lists cannot.",
        "category": "Technical",
        "difficulty": "Easy",
        "skill_reference": "Python"
    },
    {
        "question_text": "Explain Python's GIL (Global Interpreter Lock) and how it affects multi-threading.",
        "ideal_answer": "The Global Interpreter Lock (GIL) is a mutex in CPython that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once. This lock is necessary because CPython's memory management is not thread-safe. As a result, even on multi-core processors, CPU-bound multi-threaded Python programs will not run in parallel. To achieve parallelism for CPU-bound tasks, developers use multi-processing (using separate interpreter processes) instead of multi-threading, or use C-extensions that release the GIL.",
        "category": "Technical",
        "difficulty": "Hard",
        "skill_reference": "Python"
    },
    {
        "question_text": "What are decorators in Python and how do you write a custom decorator?",
        "ideal_answer": "A decorator is a design pattern in Python that allows you to modify or extend the behavior of a function or class wrapper without permanently modifying the wrapped code. They are represented by the @decorator_name syntax. Inside, a decorator takes a function as an argument, defines a nested wrapper function that executes some code before and after calling the original function, and returns this wrapper function.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "Python"
    },
    {
        "question_text": "What is generator in Python and how does it save memory?",
        "ideal_answer": "A generator is a special type of iterator in Python defined using a function with the yield keyword instead of return. Unlike lists that load all elements into memory at once, generators generate values lazily on-the-fly (one-by-one) when requested (using next() or in a loop). This lazy evaluation makes them highly memory-efficient, especially when dealing with large datasets or infinite sequences.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "Python"
    },

    # --- TECHNICAL: SQL ---
    {
        "question_text": "What is the difference between WHERE and HAVING clauses in SQL?",
        "ideal_answer": "The WHERE clause is used to filter rows before any groupings are made, based on individual row values. It cannot be used with aggregate functions like SUM, AVG, or COUNT. The HAVING clause is used to filter groups formed by the GROUP BY clause, based on aggregate conditions. WHERE filters rows; HAVING filters groups.",
        "category": "Technical",
        "difficulty": "Easy",
        "skill_reference": "SQL"
    },
    {
        "question_text": "What are SQL joins? Explain INNER, LEFT, RIGHT, and FULL joins.",
        "ideal_answer": "SQL Joins combine rows from two or more tables based on a related column. INNER JOIN returns rows with matching values in both tables. LEFT JOIN (or LEFT OUTER JOIN) returns all rows from the left table and matched rows from the right; unmatched right rows result in NULLs. RIGHT JOIN returns all rows from the right table and matched rows from the left. FULL JOIN returns all records when there is a match in either left or right table, filling unmatched columns with NULL.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "SQL"
    },
    {
        "question_text": "Explain database normalization and its forms up to 3NF.",
        "ideal_answer": "Database normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. First Normal Form (1NF) requires atomic values and unique row keys. Second Normal Form (2NF) requires meeting 1NF and ensuring all non-key attributes are fully dependent on the primary key (no partial dependency). Third Normal Form (3NF) requires meeting 2NF and removing transitive dependencies, meaning non-key fields must depend only on the primary key.",
        "category": "Technical",
        "difficulty": "Hard",
        "skill_reference": "SQL"
    },

    # --- TECHNICAL: MACHINE LEARNING & DATA SCIENCE ---
    {
        "question_text": "What is the difference between Overfitting and Underfitting, and how do you address them?",
        "ideal_answer": "Overfitting occurs when a model learns the training data too well, including its noise and outliers, resulting in high training accuracy but poor generalization to unseen data (high variance). It is addressed by regularization (L1/L2), cross-validation, pruning, or adding more training data. Underfitting occurs when the model is too simple to capture the underlying pattern of the data (high bias). It is resolved by increasing model complexity, adding more relevant features, or reducing regularization.",
        "category": "Technical",
        "difficulty": "Easy",
        "skill_reference": "Machine Learning"
    },
    {
        "question_text": "Explain the Bias-Variance Tradeoff.",
        "ideal_answer": "The bias-variance tradeoff is a fundamental concept in machine learning describing the tension between bias (error from erroneous assumptions, leading to underfitting) and variance (error from sensitivity to small fluctuations in training data, leading to overfitting). As model complexity increases, bias decreases but variance increases. The goal is to find the sweet spot where total prediction error is minimized, achieving a balanced model that generalizes well.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "Machine Learning"
    },
    {
        "question_text": "How does Random Forest work, and how is it different from Decision Trees?",
        "ideal_answer": "A Decision Tree is a single classifier that splits data recursively based on feature values to make predictions. Random Forest is an ensemble learning method that builds multiple decision trees during training. It uses bagging (bootstrap aggregating) to train each tree on random subsets of the data and uses random subsets of features at each split. The final prediction is made by averaging (regression) or majority voting (classification) across all trees, which reduces variance and prevents overfitting compared to a single tree.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "Machine Learning"
    },
    {
        "question_text": "What is regularization? Explain L1 (Lasso) and L2 (Ridge) regularization.",
        "ideal_answer": "Regularization is a technique used to prevent overfitting by adding a penalty term to the loss function to constrain model weights. L1 regularization (Lasso) adds a penalty equal to the absolute value of the coefficients, forcing some weights to become exactly zero, which performs automatic feature selection. L2 regularization (Ridge) adds a penalty equal to the square of the coefficients, shrinking weights close to zero but not completely, which helps manage multicollinearity and keeps weights small.",
        "category": "Technical",
        "difficulty": "Hard",
        "skill_reference": "Machine Learning"
    },

    # --- TECHNICAL: DEEP LEARNING & NLP ---
    {
        "question_text": "What is the role of activation functions in Neural Networks?",
        "ideal_answer": "Activation functions introduce non-linearity into neural networks, enabling them to learn complex patterns and solve non-linear problems. Without activation functions, a neural network, no matter how many layers it has, would behave like a simple linear regression model because linear combinations of linear functions are always linear. Common activation functions include ReLU, Sigmoid, Tanh, and Softmax.",
        "category": "Technical",
        "difficulty": "Easy",
        "skill_reference": "Deep Learning"
    },
    {
        "question_text": "What is the Vanishing Gradient problem and how can it be resolved?",
        "ideal_answer": "The vanishing gradient problem occurs during backpropagation in deep neural networks when gradients shrink exponentially as they propagate backward through layers. This causes weights in early layers to update very slowly or not at all, halting learning. It is resolved using activation functions like ReLU (which doesn't saturate for positive inputs), batch normalization, residual connections (as in ResNets), and proper weight initialization techniques like Xavier or He initialization.",
        "category": "Technical",
        "difficulty": "Hard",
        "skill_reference": "Deep Learning"
    },
    {
        "question_text": "What is TF-IDF and how is it calculated?",
        "ideal_answer": "TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a statistical measure used to evaluate how important a word is to a document in a collection or corpus. Term Frequency (TF) measures the frequency of a word in a specific document. Inverse Document Frequency (IDF) measures how common or rare a word is across all documents in the corpus, calculated as the logarithm of total documents divided by documents containing the term. TF-IDF is the product of TF and IDF.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "NLP"
    },
    {
        "question_text": "Explain Word Embeddings and the difference between Word2Vec and BERT.",
        "ideal_answer": "Word embeddings are dense vector representations of words where words with similar meanings are close in the vector space. Word2Vec produces static embeddings, meaning a word has the same vector regardless of its context (e.g., 'bank' in river bank vs. money bank). BERT (Bidirectional Encoder Representations from Transformers) produces dynamic, contextualized embeddings, meaning the vector for a word is calculated based on its surrounding words in a sentence, capturing polysemy and local context.",
        "category": "Technical",
        "difficulty": "Hard",
        "skill_reference": "NLP"
    },

    # --- TECHNICAL: JAVA ---
    {
        "question_text": "Explain the concepts of OOP in Java.",
        "ideal_answer": "Object-Oriented Programming (OOP) in Java relies on four primary concepts: Inheritance (a class acquiring properties/behaviors of a parent class using 'extends'), Polymorphism (performing a single action in different ways, e.g., method overloading and overriding), Encapsulation (wrapping data and methods into a single unit and restricting direct access using private modifiers and getter/setter methods), and Abstraction (hiding implementation details and showing only functionality using interfaces or abstract classes).",
        "category": "Technical",
        "difficulty": "Easy",
        "skill_reference": "Java"
    },
    {
        "question_text": "What is the difference between Abstract Class and Interface in Java?",
        "ideal_answer": "An abstract class can have both abstract (without body) and concrete (with body) methods, state (instance variables), and constructors. A class can extend only one abstract class. An interface, prior to Java 8, could only have abstract methods and static final variables. In Java 8 and later, interfaces can have default and static methods. A class can implement multiple interfaces. Abstract classes represent an 'is-a' relationship and share state, while interfaces represent a 'can-do' contract.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "Java"
    },

    # --- TECHNICAL: WEB DEVELOPMENT ---
    {
        "question_text": "What is the difference between Virtual DOM and Real DOM in React?",
        "ideal_answer": "The Real DOM represents the browser's HTML structure. Updating the Real DOM is slow because it triggers layout recalculations and repainting. The Virtual DOM is a lightweight, in-memory representation of the Real DOM used by React. When a component state changes, React updates the Virtual DOM first, compares it with a snapshot of the previous Virtual DOM using a diffing algorithm (reconciliation), and updates only the changed elements in the Real DOM, which improves web performance.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "React"
    },
    {
        "question_text": "What is asynchronous programming in JavaScript and what are Promises?",
        "ideal_answer": "Asynchronous programming in JavaScript allows tasks to execute in the background without blocking the main execution thread. A Promise is an object representing the eventual completion or failure of an asynchronous operation. It has three states: Pending (operation is ongoing), Fulfilled (operation completed successfully, resolving with a value), and Rejected (operation failed with an error). Promises allow chaining operations using .then() and .catch(), or handling them using async/await syntax.",
        "category": "Technical",
        "difficulty": "Medium",
        "skill_reference": "JavaScript"
    },

    # --- HR QUESTIONS ---
    {
        "question_text": "Tell me about yourself.",
        "ideal_answer": "A strong answer should follow the Present-Past-Future formula. Talk briefly about your current role, key responsibilities, and recent achievements. Then, explain the academic or professional path that led you here, focusing on relevant skills you developed. Finally, explain why you are excited about this specific opportunity and how it aligns with your career goals.",
        "category": "HR",
        "difficulty": "Easy",
        "skill_reference": "HR"
    },
    {
        "question_text": "What are your greatest strengths and weaknesses?",
        "ideal_answer": "For strengths, focus on professional traits backed by examples, such as problem-solving skills, quick learning, or teamwork. For weaknesses, pick a real but non-critical skill that you have actively worked to improve. Describe the steps you took (e.g., taking a course, implementing a tool) to show self-awareness, honesty, and a commitment to personal growth.",
        "category": "HR",
        "difficulty": "Easy",
        "skill_reference": "HR"
    },
    {
        "question_text": "Why do you want to work for our company?",
        "ideal_answer": "Show that you have researched the company. Mention their products, services, recent news, or company culture that resonates with you. Connect their mission or goals with your own professional values and career path to show that you are motivated by more than just a paycheck.",
        "category": "HR",
        "difficulty": "Easy",
        "skill_reference": "HR"
    },
    {
        "question_text": "Where do you see yourself in five years?",
        "ideal_answer": "Express a desire to grow your skills, take on more responsibility, and make a significant contribution to the company. Frame your answer to show that you want to grow *within* this organization, possibly transitioning into a senior developer, tech lead, or specialist role, indicating long-term commitment.",
        "category": "HR",
        "difficulty": "Medium",
        "skill_reference": "HR"
    },

    # --- BEHAVIORAL QUESTIONS ---
    {
        "question_text": "Describe a time when you had to work with a difficult team member. How did you handle it?",
        "ideal_answer": "Use the STAR method (Situation, Task, Action, Result). Describe the challenge objectively without speaking negatively about the person. Explain how you communicated openly, showed empathy, found common ground or compromised to complete the task, and describe the positive outcome of the project.",
        "category": "Behavioral",
        "difficulty": "Medium",
        "skill_reference": "Behavioral"
    },
    {
        "question_text": "Tell me about a time you failed and what you learned from it.",
        "ideal_answer": "Select a genuine mistake (not a disguised success). Explain the context, take full responsibility for the failure, and outline the immediate actions you took to fix it or mitigate the impact. Most importantly, highlight what you learned and how you changed your process or behavior to ensure it never happened again.",
        "category": "Behavioral",
        "difficulty": "Medium",
        "skill_reference": "Behavioral"
    },
    {
        "question_text": "Describe a situation where you had to meet a tight deadline under pressure.",
        "ideal_answer": "Explain the situation, how you prioritized tasks, managed your time (e.g., breaking the task into milestones), and communicated progress to team members or stakeholders. Focus on how you maintained high quality work while meeting the deadline successfully.",
        "category": "Behavioral",
        "difficulty": "Medium",
        "skill_reference": "Behavioral"
    },

    # --- SCENARIO-BASED QUESTIONS ---
    {
        "question_text": "You notice a critical security vulnerability in a production system. How do you handle it?",
        "ideal_answer": "First, immediately document the vulnerability details and report it to the security team and engineering manager. Next, assess the scope and potential impact on user data. Work to isolate the affected system if possible without causing excessive downtime. Create and test a hotfix in a staging environment, deploy the patch, verify the fix, and write a post-mortem report to prevent similar issues in the future.",
        "category": "Scenario",
        "difficulty": "Hard",
        "skill_reference": "Scenario"
    },
    {
        "question_text": "A client requests a major feature change two days before the scheduled product release. What do you do?",
        "ideal_answer": "I would acknowledge the request and schedule a meeting with the client, product manager, and tech lead. I would explain the impact of the late change on the timeline, quality, and budget. I'd propose two options: release the current stable version on time and deliver the new feature in a fast-follow update, or delay the release to incorporate the change if it is critical. This ensures expectation management and maintains trust.",
        "category": "Scenario",
        "difficulty": "Hard",
        "skill_reference": "Scenario"
    }
]

# Let's add more questions programmatically to enrich the bank
extra_topics = [
    ("Git", "What is the difference between git merge and git rebase?", 
     "Git merge combines changes from two branches by creating a new merge commit, preserving the historical timeline of branches. Git rebase moves the base of a branch to a new starting point, rewriting project history by applying commits one by one. Merge is non-destructive, whereas rebase creates a clean, linear commit history but can require force pushing and should be avoided on public/shared branches.", "Medium"),
    ("Pandas", "How do you handle missing values in a Pandas DataFrame?", 
     "Missing values (NaN) can be handled by identifying them using .isna() or .isnull(). They can be removed using .dropna() (either dropping rows or columns), or filled using .fillna() with a default value, the mean/median/mode, or using forward/backward fill (.ffill()/.bfill()). Alternatively, missing values can be interpolated using .interpolate() for continuous time-series data.", "Easy"),
    ("NumPy", "What is broadcasting in NumPy?", 
     "Broadcasting is a mechanism in NumPy that allows arithmetic operations between arrays of different shapes. NumPy compares their shapes element-wise starting from the trailing dimensions. Two dimensions are compatible if they are equal, or if one of them is 1. This allows smaller arrays to be 'broadcast' across larger arrays without copying data, making operations fast and memory-efficient.", "Medium"),
    ("Scikit-learn", "What is the purpose of a Pipeline in Scikit-learn?", 
     "A Pipeline allows you to chain multiple data preprocessing steps (like scaling, imputation, encoding) and a final machine learning estimator into a single object. This helps avoid data leakage (e.g., fitting scalers on test data) during cross-validation, enforces a clean execution sequence, and makes code modular, reusable, and easy to deploy.", "Medium"),
    ("TensorFlow", "What is the difference between a dense layer and a convolutional layer?", 
     "A Dense (fully connected) layer connects every input neuron to every output neuron, learning global patterns across all inputs. A Convolutional layer (Conv2D) applies local filters (kernels) to spatial dimensions of the input (like images), sharing weights across different positions to learn local features like edges, textures, and shapes while preserving spatial relationships and using fewer parameters.", "Hard"),
    ("PyTorch", "What does loss.backward() and optimizer.step() do in PyTorch?", 
     "loss.backward() computes the gradient of the loss function with respect to all model parameters (tensors that have requires_grad=True) using backpropagation, storing these gradients in the .grad attribute of each tensor. optimizer.step() uses these stored gradients to update the model weights based on the optimization algorithm (e.g., SGD, Adam). Before calculating gradients, optimizer.zero_grad() is called to clear previous gradients.", "Hard"),
    ("Tableau", "What is the difference between Dimensions and Measures in Tableau?", 
     "Dimensions are qualitative or categorical data (e.g., Name, Date, Region) that partition and group the data. They display as blue fields. Measures are quantitative or numerical data (e.g., Sales, Profit, Temperature) that can be aggregated mathematically (summed, averaged). They display as green fields.", "Easy"),
    ("Power BI", "What is DAX and what is the difference between calculated columns and measures?", 
     "DAX (Data Analysis Expressions) is the formula language in Power BI. Calculated columns are evaluated row-by-row during data refresh and stored in the model, consuming memory. Measures are calculated dynamically on-the-fly when added to a visual, evaluated based on the filter context of the visual, and do not consume storage memory.", "Medium"),
    ("Excel", "Explain the difference between VLOOKUP and XLOOKUP in Excel.", 
     "VLOOKUP searches for a value in the leftmost column of a range and returns a value in the same row from a specified column index, working only from left to right. XLOOKUP is a modern replacement that can look up values in any direction (left or right), uses exact matching by default, allows specifying fallback values for missing items, and is faster and more robust.", "Easy"),
    ("HTML", "What is semantic HTML and why is it important?", 
     "Semantic HTML uses elements that clearly describe their meaning and purpose to both the browser and the developer (e.g., <header>, <nav>, <main>, <article>, <footer>) instead of generic elements like <div> or <span>. It is important because it improves SEO, accessibility for screen readers, and code readability.", "Easy"),
    ("CSS", "What is the difference between CSS Flexbox and Grid?", 
     "CSS Flexbox is a one-dimensional layout system designed for laying out items in a single row or column. It handles alignment, space distribution, and wrapping. CSS Grid is a two-dimensional layout system designed for complex layouts with rows and columns. Flexbox is content-driven, whereas Grid is layout-driven.", "Easy"),
    ("Node.js", "Explain the event loop in Node.js.", 
     "The event loop is a mechanism that allows Node.js to perform non-blocking, asynchronous I/O operations despite JavaScript being single-threaded. It works by offloading I/O tasks to the operating system or worker threads via libuv. When a task completes, it is placed in a callback queue. The event loop continuously monitors the call stack and moves callbacks to the stack when the stack is empty.", "Hard"),
    ("Git", "What is git stash and when would you use it?", 
     "git stash saves your local modifications (staged and unstaged) in a temporary storage area, reverting the working directory to match the HEAD commit. This is useful when you have unfinished work in progress and need to switch branches, pull remote updates, or fix an urgent bug without committing incomplete code.", "Easy")
]

for skill, q, ans, diff in extra_topics:
    QUESTIONS.append({
        "question_text": q,
        "ideal_answer": ans,
        "category": "Technical",
        "difficulty": diff,
        "skill_reference": skill
    })

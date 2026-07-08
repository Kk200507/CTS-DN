-- =====================================================================
-- Module 3: Database - Advanced SQL Examples
-- =====================================================================
-- This file contains SQL examples demonstrating advanced relational queries.
-- These concepts are critical for backend developers handling complex data
-- aggregation, hierarchical structures, and analytical reporting.
-- ---------------------------------------------------------------------

-- Setup Sample Schema (for visualization/understanding of the examples)
-- CREATE TABLE employees (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100),
--     department_id INT,
--     salary NUMERIC(10, 2),
--     manager_id INT
-- );

-- =====================================================================
-- 1. Window Functions
-- =====================================================================
-- Window functions perform a calculation across a set of table rows that are 
-- related to the current row, without grouping the output into a single row.

-- Example: Ranking employees within their department by salary, and computing 
-- the running sum of salaries inside each department.
SELECT 
    name,
    department_id,
    salary,
    -- ROW_NUMBER() assigns a unique sequential integer starting from 1
    ROW_NUMBER() OVER(PARTITION BY department_id ORDER BY salary DESC) as rank_by_row,
    
    -- RANK() assigns ranking, skips ranks on ties (e.g., 1, 2, 2, 4)
    RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) as rank_with_skips,
    
    -- DENSE_RANK() assigns ranking, does not skip ranks on ties (e.g., 1, 2, 2, 3)
    DENSE_RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) as dense_rank,
    
    -- Running total of salaries within the department
    SUM(salary) OVER(PARTITION BY department_id ORDER BY salary ASC 
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_department_total
FROM employees;


-- =====================================================================
-- 2. Common Table Expressions (CTEs)
-- =====================================================================
-- CTEs provide a way to write auxiliary statements for use in a larger query.
-- They act as temporary views defined only for the execution of that query.

-- A. Non-Recursive CTE (Simplifying complex query logic)
WITH DepartmentStats AS (
    SELECT 
        department_id,
        AVG(salary) as avg_dept_salary,
        COUNT(*) as employee_count
    FROM employees
    GROUP BY department_id
)
SELECT 
    e.name,
    e.salary,
    ds.avg_dept_salary,
    e.salary - ds.avg_dept_salary as salary_diff_from_avg
FROM employees e
JOIN DepartmentStats ds ON e.department_id = ds.department_id
WHERE e.salary > ds.avg_dept_salary;

-- B. Recursive CTE (For hierarchical or tree-structured data like Org Charts)
-- Finds the management hierarchy (path) for all employees starting from the CEO.
WITH RECURSIVE OrgChart AS (
    -- Anchor member: Start with top-level managers (manager_id is NULL)
    SELECT 
        id, 
        name, 
        manager_id, 
        1 as level,
        CAST(name AS VARCHAR(255)) as hierarchy_path
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive member: Join employees with their managers in the OrgChart CTE
    SELECT 
        e.id, 
        e.name, 
        e.manager_id, 
        oc.level + 1,
        CAST(oc.hierarchy_path || ' -> ' || e.name AS VARCHAR(255))
    FROM employees e
    JOIN OrgChart oc ON e.manager_id = oc.id
)
SELECT id, name, manager_id, level, hierarchy_path 
FROM OrgChart 
ORDER BY level, id;


-- =====================================================================
-- 3. Advanced Joins
-- =====================================================================

-- A. Self Join: Joining a table to itself (e.g., matching employees to managers)
SELECT 
    emp.name as employee_name,
    mgr.name as manager_name
FROM employees emp
LEFT JOIN employees mgr ON emp.manager_id = mgr.id;

-- B. Full Outer Join: Returns all rows when there is a match in either table
-- SELECT * FROM project_assignments p FULL OUTER JOIN employees e ON p.employee_id = e.id;

-- C. Cross Join: Cartesian product of two tables (combinations of all records)
-- SELECT s.size, c.color FROM sizes s CROSS JOIN colors c;


-- =====================================================================
-- 4. Subqueries: Correlated vs. Non-Correlated
-- =====================================================================

-- A. Non-Correlated Subquery: Executed once, independent of the outer query.
-- Finds employees earning more than the overall average salary.
SELECT name, salary 
FROM employees 
WHERE salary > (SELECT AVG(salary) FROM employees);

-- B. Correlated Subquery: Executed once for each row evaluated by the outer query.
-- Finds employees who earn more than the average salary of their specific department.
SELECT name, salary, department_id
FROM employees e
WHERE salary > (
    SELECT AVG(salary) 
    FROM employees 
    WHERE department_id = e.department_id
);


-- =====================================================================
-- 5. Grouping Sets, Rollup, and Cube
-- =====================================================================
-- These extensions to the GROUP BY clause compute multiple grouping sets in a single query.
-- Useful for generating multi-dimensional report dashboards.

-- Setup context: Aggregating sales data across region and product categories
-- SELECT 
--     region, 
--     category, 
--     SUM(amount) as total_sales
-- FROM sales
-- GROUP BY GROUPING SETS ((region, category), (region), (category), ());

-- ROLLUP: Creates hierarchical sub-totals (e.g., (region, category), (region), ())
-- SELECT region, category, SUM(amount) FROM sales GROUP BY ROLLUP (region, category);

-- CUBE: Creates all possible grouping combinations (e.g., (region, category), (region), (category), ())
-- SELECT region, category, SUM(amount) FROM sales GROUP BY CUBE (region, category);

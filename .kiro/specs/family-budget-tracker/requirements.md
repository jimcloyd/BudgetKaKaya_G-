# Requirements Document

## Introduction

This document outlines the requirements for a Family Budget Tracker system that enables a married couple to collaboratively manage their household expenses, track spending, and maintain a shared budget.

## Glossary

- **Budget Tracker**: The software system that manages household financial tracking
- **User**: An individual (spouse) who uses the Budget Tracker
- **Expense**: A financial transaction representing money spent
- **Budget Category**: A classification for grouping related expenses (e.g., groceries, utilities, entertainment)
- **Budget Limit**: The maximum amount allocated for a specific category within a time period
- **Shared Account**: The household financial account accessible to both spouses
- **Installment**: A recurring payment obligation for a credit card purchase divided into multiple payments
- **Savings Goal**: A designated amount of money being accumulated for a specific purpose (e.g., MP2, emergency fund)
- **Credit Card**: A payment card with an associated balance and credit limit
- **Credit Card Balance**: The total amount owed on a Credit Card
- **Monthly Income**: The total gross income received by the household in a month
- **Password Reset Token**: A unique, time-limited token sent via email to verify password reset requests

## Requirements

### Requirement 1

**User Story:** As a new user, I want to create an account and log in, so that I can access the budget tracker securely

#### Acceptance Criteria

1. WHEN a new User provides email address, password, password confirmation, and name, THE Budget Tracker SHALL create a user account
2. THE Budget Tracker SHALL require password to be at least 8 characters long
3. THE Budget Tracker SHALL verify that password and password confirmation match before creating an account
4. THE Budget Tracker SHALL verify that the email address is unique before creating an account
5. WHEN a User provides valid credentials, THE Budget Tracker SHALL authenticate the User and grant access to their account
6. WHEN a User provides invalid credentials, THE Budget Tracker SHALL display an error message and deny access

### Requirement 2

**User Story:** As a user, I want to invite my spouse to share a budget account, so that we can manage our finances together

#### Acceptance Criteria

1. WHEN a User sends an invitation with a spouse email address, THE Budget Tracker SHALL create a pending invitation
2. WHEN the invited spouse accepts the invitation, THE Budget Tracker SHALL link both User accounts to the same Shared Account
3. THE Budget Tracker SHALL allow a maximum of two Users per Shared Account
4. THE Budget Tracker SHALL require the invited User to have an existing account or create one before accepting the invitation
5. WHEN Users are linked to a Shared Account, THE Budget Tracker SHALL grant both Users equal access to all shared financial data

### Requirement 3

**User Story:** As a spouse, I want to record our household expenses, so that we can track where our money is going

#### Acceptance Criteria

1. WHEN a User submits an expense entry with amount, category, date, and description, THE Budget Tracker SHALL store the expense in the Shared Account
2. THE Budget Tracker SHALL require amount, category, and date fields for each expense entry
3. WHEN a User enters an expense amount, THE Budget Tracker SHALL accept positive numerical values with up to two decimal places
4. THE Budget Tracker SHALL display all recorded expenses in chronological order with most recent first
5. WHEN a User views the expense list, THE Budget Tracker SHALL show the amount, category, date, description, and which spouse entered it

### Requirement 4

**User Story:** As a spouse, I want to categorize our expenses, so that we can understand our spending patterns

#### Acceptance Criteria

1. THE Budget Tracker SHALL provide predefined categories including groceries, utilities, transportation, entertainment, healthcare, and miscellaneous
2. WHEN a User creates an expense, THE Budget Tracker SHALL require selection of exactly one category
3. THE Budget Tracker SHALL allow Users to add custom categories with unique names
4. WHEN a User views spending summary, THE Budget Tracker SHALL display total amount spent per category for the selected time period
5. THE Budget Tracker SHALL calculate and display the percentage of total spending for each category

### Requirement 5

**User Story:** As a spouse, I want to set budget limits for different categories, so that we can control our spending

#### Acceptance Criteria

1. WHEN a User sets a Budget Limit for a category, THE Budget Tracker SHALL store the limit amount and associated time period
2. THE Budget Tracker SHALL support monthly and weekly time periods for Budget Limits
3. WHEN spending in a category reaches 80 percent of the Budget Limit, THE Budget Tracker SHALL display a warning indicator
4. WHEN spending in a category exceeds the Budget Limit, THE Budget Tracker SHALL display an alert indicator
5. THE Budget Tracker SHALL show remaining budget amount for each category with an active Budget Limit

### Requirement 6

**User Story:** As a spouse, I want to see our total spending over time, so that we can monitor our financial health

#### Acceptance Criteria

1. THE Budget Tracker SHALL calculate total expenses for the current month
2. WHEN a User selects a date range, THE Budget Tracker SHALL display total spending for that period
3. THE Budget Tracker SHALL provide filtering options by category, date range, and spouse
4. WHEN a User views the dashboard, THE Budget Tracker SHALL display a summary showing total spent, total budget, and remaining budget
5. THE Budget Tracker SHALL calculate and display month-over-month spending comparison

### Requirement 7

**User Story:** As a spouse, I want to edit or delete expenses, so that we can correct mistakes

#### Acceptance Criteria

1. WHEN a User selects an existing expense, THE Budget Tracker SHALL provide options to edit or delete the expense
2. WHEN a User modifies an expense, THE Budget Tracker SHALL update the expense with the new values and maintain the original creation timestamp
3. WHEN a User deletes an expense, THE Budget Tracker SHALL remove the expense from all calculations and displays
4. THE Budget Tracker SHALL allow any User in the Shared Account to edit or delete any expense regardless of who created it
5. WHEN an expense is modified or deleted, THE Budget Tracker SHALL recalculate all affected category totals and budget status

### Requirement 8

**User Story:** As a spouse, I want to track credit card installment payments, so that we can manage our payment obligations

#### Acceptance Criteria

1. WHEN a User creates an Installment, THE Budget Tracker SHALL require total amount, number of payments, start date, and description
2. THE Budget Tracker SHALL calculate the monthly payment amount by dividing total amount by number of payments
3. WHEN an Installment payment date arrives, THE Budget Tracker SHALL display the payment as due in the current month expenses
4. THE Budget Tracker SHALL track which Installment payments have been completed and which remain outstanding
5. WHEN a User views Installments, THE Budget Tracker SHALL display remaining balance, next payment date, and monthly payment amount

### Requirement 9

**User Story:** As a spouse, I want to track our savings contributions, so that we can monitor progress toward our financial goals

#### Acceptance Criteria

1. WHEN a User creates a Savings Goal, THE Budget Tracker SHALL require goal name, target amount, and optional target date
2. THE Budget Tracker SHALL allow Users to record savings contributions with amount and date
3. WHEN a User views a Savings Goal, THE Budget Tracker SHALL display current balance, target amount, and percentage completed
4. THE Budget Tracker SHALL calculate remaining amount needed to reach each Savings Goal
5. WHERE a Savings Goal has a target date, THE Budget Tracker SHALL display suggested monthly contribution amount to reach the goal on time

### Requirement 10

**User Story:** As a spouse, I want to track our credit card balances, so that we can monitor our debt and available credit

#### Acceptance Criteria

1. WHEN a User adds a Credit Card, THE Budget Tracker SHALL require card name, credit limit, and current balance
2. THE Budget Tracker SHALL calculate available credit by subtracting Credit Card Balance from credit limit
3. WHEN a User records a credit card payment, THE Budget Tracker SHALL reduce the Credit Card Balance by the payment amount
4. WHEN a User records a credit card charge, THE Budget Tracker SHALL increase the Credit Card Balance by the charge amount
5. WHEN a User views Credit Cards, THE Budget Tracker SHALL display card name, current balance, credit limit, and available credit for each card

### Requirement 11

**User Story:** As a spouse, I want to track our monthly income and compare it to expenses, so that we can see if we are living within our means

#### Acceptance Criteria

1. WHEN a User enters Monthly Income, THE Budget Tracker SHALL store the gross income amount for the specified month
2. THE Budget Tracker SHALL allow Users to update Monthly Income for any month
3. WHEN a User views the dashboard, THE Budget Tracker SHALL display a chart comparing Monthly Income to total expenses for the current month
4. THE Budget Tracker SHALL calculate net income by subtracting total expenses from Monthly Income
5. WHEN net income is negative, THE Budget Tracker SHALL display the amount in red to indicate overspending

### Requirement 12

**User Story:** As a user, I want to reset my password if I forget it, so that I can regain access to my account

#### Acceptance Criteria

1. WHEN a User requests a password reset with their email address, THE Budget Tracker SHALL generate a unique Password Reset Token
2. THE Budget Tracker SHALL send an email containing the Password Reset Token link to the User email address within 60 seconds
3. THE Budget Tracker SHALL expire the Password Reset Token after 1 hour from generation
4. WHEN a User clicks the Password Reset Token link and provides a new password with confirmation, THE Budget Tracker SHALL update the User password
5. THE Budget Tracker SHALL invalidate the Password Reset Token after successful password reset or after expiration

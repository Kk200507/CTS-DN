/**
 * Angular & TypeScript Demonstration File
 * 
 * This file illustrates TypeScript fundamentals and representative code 
 * structures for Angular components, modules, services, reactive forms, 
 * HTTP client requests, and RxJS pipelines.
 */

// ==============================================================================
// 1. TYPESCRIPT BASICS (Interfaces, Types, and Classes)
// ==============================================================================

// Interface defining a strict schema for a User object
export interface User {
    id: number;
    name: string;
    email: string;
    role: 'Admin' | 'Student' | 'Instructor'; // Union Type
    isActive: boolean;
}

// Class implementing a User creation blueprint
export class UserAccount {
    // Type annotations in constructor parameters (TypeScript compiler converts to property assignments)
    constructor(
        public username: string,
        private secretToken: string
    ) {}

    public getSecretPrefix(): string {
        return this.secretToken.substring(0, 4) + '...';
    }
}


// Mock imports simulating Angular framework decorator imports
// (Presented statically for educational structure)
const Component = (config: any) => (cls: any) => {};
const Injectable = (config?: any) => (cls: any) => {};
const NgModule = (config: any) => (cls: any) => {};


// ==============================================================================
// 2. ANGULAR SERVICES & DEPENDENCY INJECTION (DI)
// ==============================================================================

// Dummy classes representing Angular modules for type checking
class HttpClient {
    get(url: string) { return { pipe: (arg: any) => {} }; }
}
class FormBuilder {
    group(config: any) { return { value: {}, valid: true }; }
}
interface Observable<T> {
    subscribe(callback: (val: T) => void): void;
}

@Injectable({
    providedIn: 'root' // Declares service globally available for DI injection
})
export class UserService {
    private apiUrl = 'https://api.example.com/users';

    // HttpClient is injected via the constructor (Dependency Injection)
    constructor(private http: HttpClient) {}

    /**
     * Fetches user data as an RxJS Observable stream.
     */
    public getUsers(): Observable<User[]> {
        // http.get automatically returns an Observable stream
        return this.http.get(this.apiUrl) as any;
    }
}


// ==============================================================================
// 3. ANGULAR COMPONENT
// ==============================================================================

@Component({
    selector: 'app-user-profile',
    template: `
        <div class="profile-container">
            <h2>User Profile List</h2>
            <ul>
                <li *ngFor="let user of users">
                    {{ user.name }} ({{ user.role }}) - {{ user.email }}
                </li>
            </ul>
            
            <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
                <input formControlName="name" placeholder="Enter name">
                <button type="submit" [disabled]="!userForm.valid">Add User</button>
            </form>
        </div>
    `,
    styles: [`
        .profile-container { padding: 20px; border: 1px solid #ddd; }
    `]
})
export class UserProfileComponent {
    public users: User[] = [];
    public userForm: any;

    // Injecting dependencies into Component
    constructor(
        private userService: UserService,
        private fb: FormBuilder
    ) {
        this.initializeForm();
    }

    // Lifecycle hook equivalent
    public ngOnInit(): void {
        // RxJS Observables must be subscribed to in order to trigger execution
        this.userService.getUsers().subscribe({
            next: (data) => {
                this.users = data;
            },
            error: (err) => console.error('Error fetching users:', err)
        });
    }

    private initializeForm(): void {
        // Reactive Forms: Declaring form structure with validation rules
        this.userForm = this.fb.group({
            name: ['', /* validators could go here: Validators.required */],
            email: ['', /* Validators.email */]
        });
    }

    public onSubmit(): void {
        if (this.userForm.valid) {
            console.log('Submitted reactive form data:', this.userForm.value);
        }
    }
}


// ==============================================================================
// 4. ANGULAR MODULES
// ==============================================================================

@NgModule({
    declarations: [
        UserProfileComponent // Components belonging to this module
    ],
    imports: [
        // Standard modules imported (e.g. BrowserModule, ReactiveFormsModule, HttpClientModule)
    ],
    providers: [
        UserService // Services instantiated for DI
    ],
    bootstrap: [UserProfileComponent]
})
export class AppModule {}


// ==============================================================================
// 5. RXJS OBSERVABLES & OPERATORS EXPLANATION
// ==============================================================================
/*
RxJS is a library for reactive programming using Observables to compose asynchronous code.

Key Operators:
  - map(): Transforms values emitted by Observable.
  - filter(): Emits only values passing a criteria.
  - catchError(): Catches errors on source Observable to return fallbacks.

Pipeline usage example:
--------------------------------------------------------------------------------
import { map, filter } from 'rxjs/operators';

this.userService.getUsers()
    .pipe(
        // Filter out inactive users
        map(users => users.filter(u => u.isActive)),
        // Map to names string list
        map(activeUsers => activeUsers.map(u => u.name))
    )
    .subscribe(names => console.log('Active user names:', names));
*/


// ==============================================================================
// 6. ANGULAR ROUTING SUMMARY
// ==============================================================================
/*
Routing is configured as a list of Route paths mapping to components.

Example Configuration:
--------------------------------------------------------------------------------
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
    { path: '', redirectTo: '/welcome', pathMatch: 'full' },
    { path: 'welcome', component: WelcomeComponent },
    { path: 'users', component: UserProfileComponent },
    { path: '**', component: PageNotFoundComponent } // Wildcard fallback
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}
*/

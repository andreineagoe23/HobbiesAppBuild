import { Hobby } from './Hobby';

export interface User {
  id: number;
  name: string;
  email: string;
  dob: string;
  hobbies: Hobby[];
}

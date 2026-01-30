import { Injectable } from '@angular/core';
import { AccountService } from './account.service';
import { ApplicationUser } from '../models/application-user';


@Injectable({
  providedIn: 'root'
})
export class AuditFieldsService {

  private applicationUser : ApplicationUser  | null = null;

  constructor(private accountService: AccountService) {
    const currentUser  = this.accountService.getCurrentUser ();
    if (currentUser ) {
      this.applicationUser  = currentUser ;
    }
  }
  appendAuditFields<T extends Record<string, any>>(obj: T): T {
    const now = new Date();
    (obj as any)['CreatedOn'] = (obj as any)['CreatedOn'] || now;
    (obj as any)['CreatedBy'] = (obj as any)['CreatedBy'] || (this.applicationUser ?.id || null);
    (obj as any)['ModifiedOn'] = now; 
    (obj as any)['ModifiedBy'] = this.applicationUser ?.id || null;
    (obj as any)['IsActive'] = (obj as any)['IsActive'] !== undefined ? (obj as any)['IsActive'] : true; 
    return obj;
  }
}
import { Injectable } from '@angular/core';
import { ApiService } from '../../common/services/api.service';
import { Observable } from 'rxjs';
import { MonthlySalary } from '../models/monlty_salary';
import { environment } from '../../../environment';
import { MonthlySalaryDetails } from '../models/monlty_salary.details';

@Injectable({
  providedIn: 'root',
})
export class MonthlySalaryService {
  http: any;
  constructor(private apiService: ApiService) {}

  GetMonthlySalaryListAsync(): Observable<MonthlySalary[]> {
    return this.apiService.send<MonthlySalary[]>(
      'GET',
      environment.UrlConstants.MonthlySalary.GetMonthySalaryList,
    );
  }

  GetMonthlySalaryAsync(
    monthlySalaryId: number,
  ): Observable<MonthlySalaryDetails> {
    return this.apiService.send<MonthlySalaryDetails>(
      'GET',
      `${environment.UrlConstants.MonthlySalary.GetMonthlySalaryAsync}/${monthlySalaryId}`,
    );
  }

  // InsertOrUpdateMonthlySalaryAsync(
  //   monthlySalary: MonthlySalary,
  // ): Observable<MonthlySalary> {
  //   return this.apiService.send<MonthlySalary>(
  //     'POST',
  //     environment.UrlConstants.MonthlySalary.InsertOrUpdateMonthlySalaryAsync,
  //     monthlySalary,
  //   );
  // }
  publishMonthlySalaryAsync(monthlySalary: any) {
    return this.http.post(
      `${environment.UrlConstants.MonthlySalary.InsertOrUpdateMonthlySalaryAsync}`,
      monthlySalary,
    );
  }

  DeleteMonthlySalaryAsync(monthlySalaryId: number): Observable<any> {
    return this.apiService.send<any>(
      'DELETE',
      `${environment.UrlConstants.MonthlySalary.DeleteMonthlySalaryAsync}/${monthlySalaryId}`,
    );
  }
}

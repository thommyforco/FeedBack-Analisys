import {Pipe, PipeTransform} from '@angular/core';
interface Feedback {
    id :  number;
    testo : String;
    sentiment:String;
    categoria: String;
    dataCreazione: Date;

}
@Pipe({
  name: 'sentimentCount',
  standalone: true
})
export class SentimentCountPipe implements PipeTransform {
    transform(feedbacks:Feedback[], sentiment: string): number {
        return feedbacks.filter(f => f.sentiment === sentiment).length;
    }
}
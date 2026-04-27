export interface EmailMessage {
  to: string | string[];
  subject: string;
  body?: string;
  html?: string;
  from?: string;
  cc?: string[];
  attachments?: Array<{ filename: string; content: string }>;
  sentAt: Date;
}

export interface Mailer {
  send(message: Omit<EmailMessage, 'sentAt'>): Promise<void>;
}

/**
 * Implementação fake de Mailer para testes.
 * Captura todos os emails enviados em memória — sem SMTP real.
 */
export class FakeMailer implements Mailer {
  private readonly sent: EmailMessage[] = [];

  async send(message: Omit<EmailMessage, 'sentAt'>): Promise<void> {
    this.sent.push({ ...message, sentAt: new Date() });
  }

  getSent(): EmailMessage[] {
    return [...this.sent];
  }

  getLastSent(): EmailMessage | undefined {
    return this.sent[this.sent.length - 1];
  }

  getSentTo(email: string): EmailMessage[] {
    return this.sent.filter((msg) => {
      const to = Array.isArray(msg.to) ? msg.to : [msg.to];
      return to.includes(email);
    });
  }

  assertSentTo(email: string): void {
    const messages = this.getSentTo(email);
    if (messages.length === 0) {
      throw new Error(
        `Expected email to be sent to "${email}", but got: ${JSON.stringify(
          this.sent.map((m) => m.to),
        )}`,
      );
    }
  }

  assertNotSentTo(email: string): void {
    const messages = this.getSentTo(email);
    if (messages.length > 0) {
      throw new Error(`Expected no email to be sent to "${email}", but ${messages.length} were sent.`);
    }
  }

  assertSentCount(count: number): void {
    if (this.sent.length !== count) {
      throw new Error(`Expected ${count} email(s) to be sent, but got ${this.sent.length}.`);
    }
  }

  assertNothingSent(): void {
    this.assertSentCount(0);
  }

  clear(): void {
    this.sent.length = 0;
  }
}

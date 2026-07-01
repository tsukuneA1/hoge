type Updater<T> = (current: T) => T;

export const storage = {
  get<T>(key: string, fallback: T): T {
    const raw = localStorage.getItem(key);

    if (raw === null) {
      return fallback;
    }

    try {
      return JSON.parse(raw) as T;
    } catch {
      return fallback;
    }
  },

  set<T>(key: string, value: T): void {
    localStorage.setItem(key, JSON.stringify(value));
  },

  update<T>(key: string, fallback: T, updater: Updater<T>): T {
    const current = this.get<T>(key, fallback);
    const next = updater(current);

    this.set(key, next);

    return next;
  },

  remove(key: string): void {
    localStorage.removeItem(key);
  },
};

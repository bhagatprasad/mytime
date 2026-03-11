import { ActionReducer, MetaReducer } from '@ngrx/store';
import { initialAuthState, AuthState } from './auth.state';

const SESSION_KEY = 'auth_session';

/**
 * Runs ONCE when the app boots (state === undefined).
 *
 * Flow on page refresh:
 *  1. Angular bootstraps
 *  2. NgRx initialises — state is undefined
 *  3. This meta-reducer intercepts BEFORE any reducer runs
 *  4. Reads sessionStorage, validates the payload
 *  5. Injects { user, token } into the initial state
 *  6. Store boots as if the user never left
 *
 * sessionStorage is ONLY read here and ONLY written in AuthEffects.persistSession$.
 * No component or service ever touches storage directly.
 */
export function rehydrateMetaReducer(
  reducer: ActionReducer<{ auth: AuthState }>
): ActionReducer<{ auth: AuthState }> {
  return (state, action) => {
    if (state === undefined) {
      try {
        const raw = sessionStorage.getItem(SESSION_KEY);
        if (raw) {
          const parsed = JSON.parse(raw);
          const { user, token } = parsed;

          // Validate that both user and token exist before rehydrating
          if (user && token && typeof token === 'string') {
            const rehydratedState = {
              auth: {
                ...initialAuthState,
                user,
                token,
              },
            };
            return reducer(rehydratedState, action);
          }
        }
      } catch {
        // Corrupted or tampered storage — clear it and start fresh
        try { sessionStorage.removeItem(SESSION_KEY); } catch { /* ignore */ }
      }
    }

    return reducer(state, action);
  };
}

export const metaReducers: MetaReducer[] = [
  rehydrateMetaReducer as MetaReducer,
];
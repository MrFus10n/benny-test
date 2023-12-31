/**
 * Generated by orval v6.19.1 🍺
 * Do not edit manually.
 */
import {
  useMutation,
  useQuery
} from '@tanstack/react-query'
import type {
  MutationFunction,
  QueryFunction,
  QueryKey,
  UseMutationOptions,
  UseQueryOptions,
  UseQueryResult
} from '@tanstack/react-query'
import axios from 'axios'
import type {
  AxiosError,
  AxiosRequestConfig,
  AxiosResponse
} from 'axios'
import type {
  Parser,
  User
} from '.././api/models'

// https://stackoverflow.com/questions/49579094/typescript-conditional-types-filter-out-readonly-properties-pick-only-requir/49579497#49579497
type IfEquals<X, Y, A = X, B = never> = (<T>() => T extends X ? 1 : 2) extends <
T,
>() => T extends Y ? 1 : 2
? A
: B;

type WritableKeys<T> = {
[P in keyof T]-?: IfEquals<
  { [Q in P]: T[P] },
  { -readonly [Q in P]: T[P] },
  P
>;
}[keyof T];

type UnionToIntersection<U> =
  (U extends any ? (k: U)=>void : never) extends ((k: infer I)=>void) ? I : never;
type DistributeReadOnlyOverUnions<T> = T extends any ? NonReadonly<T> : never;

type Writable<T> = Pick<T, WritableKeys<T>>;
type NonReadonly<T> = [T] extends [UnionToIntersection<T>] ? {
  [P in keyof Writable<T>]: T[P] extends object
    ? NonReadonly<NonNullable<T[P]>>
    : T[P];
} : DistributeReadOnlyOverUnions<T>;


type AwaitedInput<T> = PromiseLike<T> | T;

      type Awaited<O> = O extends AwaitedInput<infer T> ? T : never;



export const currentUser = (
     options?: AxiosRequestConfig
 ): Promise<AxiosResponse<User>> => {
    
    return axios.get(
      `/api/user/current/`,options
    );
  }


export const getCurrentUserQueryKey = () => {
    
    return [`/api/user/current/`] as const;
    }

    
export const getCurrentUserQueryOptions = <TData = Awaited<ReturnType<typeof currentUser>>, TError = AxiosError<unknown>>( options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof currentUser>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  queryOptions?.queryKey ?? getCurrentUserQueryKey();

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof currentUser>>> = ({ signal }) => currentUser({ signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof currentUser>>, TError, TData> & { queryKey: QueryKey }
}

export type CurrentUserQueryResult = NonNullable<Awaited<ReturnType<typeof currentUser>>>
export type CurrentUserQueryError = AxiosError<unknown>

export const useCurrentUser = <TData = Awaited<ReturnType<typeof currentUser>>, TError = AxiosError<unknown>>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof currentUser>>, TError, TData>>, axios?: AxiosRequestConfig}

  ):  UseQueryResult<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getCurrentUserQueryOptions(options)

  const query = useQuery(queryOptions) as  UseQueryResult<TData, TError> & { queryKey: QueryKey };

  query.queryKey = queryOptions.queryKey ;

  return query;
}

export const runParser = (
    parser: NonReadonly<Parser>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<Parser>> => {
    
    return axios.post(
      `/api/text/run/`,
      parser,options
    );
  }



export const getRunParserMutationOptions = <TError = AxiosError<unknown>,
    
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof runParser>>, TError,{data: NonReadonly<Parser>}, TContext>, axios?: AxiosRequestConfig}
): UseMutationOptions<Awaited<ReturnType<typeof runParser>>, TError,{data: NonReadonly<Parser>}, TContext> => {
 const {mutation: mutationOptions, axios: axiosOptions} = options ?? {};

      


      const mutationFn: MutationFunction<Awaited<ReturnType<typeof runParser>>, {data: NonReadonly<Parser>}> = (props) => {
          const {data} = props ?? {};

          return  runParser(data,axiosOptions)
        }

        


   return  { mutationFn, ...mutationOptions }}

    export type RunParserMutationResult = NonNullable<Awaited<ReturnType<typeof runParser>>>
    export type RunParserMutationBody = NonReadonly<Parser>
    export type RunParserMutationError = AxiosError<unknown>

    export const useRunParser = <TError = AxiosError<unknown>,
    
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof runParser>>, TError,{data: NonReadonly<Parser>}, TContext>, axios?: AxiosRequestConfig}
) => {

      const mutationOptions = getRunParserMutationOptions(options);

      return useMutation(mutationOptions);
    }
    
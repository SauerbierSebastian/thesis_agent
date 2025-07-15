import React, { useState } from 'react';
import { GetServerSideProps } from 'next';
import Layout from '../components/Layout';
import QuestionnaireForm from '../components/QuestionnaireForm';
import TimelineDisplay from '../components/TimelineDisplay';
import {
    apiService,
    UserQuestionnaireData,
    TimelineResponse,
    HealthCheck
} from '../services/api';
import { AlertCircle, CheckCircle, RefreshCw } from 'lucide-react';

interface BrainstormPageProps {
    initialHealthCheck: HealthCheck;
}

export default function BrainstormPage({ initialHealthCheck }: BrainstormPageProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [healthStatus, setHealthStatus] = useState<HealthCheck>(initialHealthCheck);

    return (
        <Layout>
            <div className="space-y-8">
                {/* Health Status Banner */}
                
            </div>
        </Layout>
    )
}

export const getServerSideProps: GetServerSideProps = async () => {
    try {
        const healthCheck = await apiService.healthCheck();

        return {
            props: {
                initialHealthCheck: healthCheck,
            },
        };
    } catch (error) {
        console.error('Failed to fetch health check:', error);

        return {
            props: {
                initialHealthCheck: {
                    status: 'error',
                    timestamp: new Date().toISOString(),
                    services: {
                        ai_service: false,
                        email_service: false,
                        config: false,
                    },
                },
            },
        };
    }
}; 